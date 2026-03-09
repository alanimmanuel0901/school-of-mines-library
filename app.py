from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from functools import wraps
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'library-management-secret-key-2024'

# Database configuration - Support both PostgreSQL (production) and SQLite (development)
database_url = os.environ.get('DATABASE_URL')

if database_url:
    # Render uses postgres:// but SQLAlchemy needs postgresql://
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    # Use SQLite for local development
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads/covers'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

db = SQLAlchemy(app)

# Add now() function to Jinja2 context
@app.context_processor
def utility_processor():
    return {'now': datetime.utcnow}

# Database Models
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    branch = db.Column(db.String(100), nullable=False)
    register_number = db.Column(db.String(50), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reservations = db.relationship('Reservation', backref='student', lazy=True)
    issued_books = db.relationship('IssuedBook', backref='student', lazy=True)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    author_born_year = db.Column(db.Integer)
    author_died_year = db.Column(db.Integer)  # Optional - None if still alive
    book_published_year = db.Column(db.Integer)
    author_description = db.Column(db.Text)
    isbn = db.Column(db.String(50), unique=True, nullable=False)
    branch_category = db.Column(db.String(100), nullable=False)
    cover_image = db.Column(db.String(200), default='default_book.png')
    total_copies = db.Column(db.Integer, default=1)
    available_copies = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reservations = db.relationship('Reservation', backref='book', lazy=True)
    issued_books = db.relationship('IssuedBook', backref='book', lazy=True)

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    request_date = db.Column(db.DateTime, default=datetime.utcnow)
    processed_date = db.Column(db.DateTime)

class IssuedBook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    issue_date = db.Column(db.DateTime, default=datetime.utcnow)
    return_date = db.Column(db.DateTime)
    due_date = db.Column(db.DateTime)
    returned = db.Column(db.Boolean, default=False)
    renewal_requests = db.relationship('RenewalRequest', backref='issued_book', lazy=True)
    
    def days_overdue(self):
        if self.returned or not self.due_date:
            return 0
        now = datetime.utcnow()
        if now > self.due_date:
            return (now - self.due_date).days
        return 0
    
    def calculate_fine(self):
        """Calculate fine at ₹5 per day overdue"""
        days = self.days_overdue()
        return days * 5 if days > 0 else 0
    
    def is_overdue(self):
        if self.returned or not self.due_date:
            return False
        return datetime.utcnow() > self.due_date

class RenewalRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    issued_book_id = db.Column(db.Integer, db.ForeignKey('issued_book.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    reason = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    request_date = db.Column(db.DateTime, default=datetime.utcnow)
    processed_date = db.Column(db.DateTime)
    student = db.relationship('Student', backref='renewal_requests')

# Helper Functions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Please login as admin to access this page.', 'error')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

def student_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'student_id' not in session:
            flash('Please login to access this page.', 'error')
            return redirect(url_for('student_login'))
        return f(*args, **kwargs)
    return decorated_function

# Routes - Main Pages
@app.route('/')
def index():
    return render_template('index.html')

# Admin Routes
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        admin = Admin.query.filter_by(username=username).first()
        if admin and check_password_hash(admin.password, password):
            session['admin_id'] = admin.id
            session['admin_username'] = admin.username
            flash('Login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        flash('Invalid username or password.', 'error')
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_id', None)
    session.pop('admin_username', None)
    flash('Logged out successfully.', 'success')
    return redirect(url_for('index'))

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    total_books = Book.query.count()
    total_students = Student.query.count()
    pending_requests = Reservation.query.filter_by(status='pending').count()
    borrowed_books = IssuedBook.query.filter_by(returned=False).count()
    pending_renewals = RenewalRequest.query.filter_by(status='pending').count()
    recent_reservations = Reservation.query.order_by(Reservation.request_date.desc()).limit(5).all()
    return render_template('admin_dashboard.html',
                         total_books=total_books,
                         total_students=total_students,
                         pending_requests=pending_requests,
                         borrowed_books=borrowed_books,
                         pending_renewals=pending_renewals,
                         recent_reservations=recent_reservations)

@app.route('/admin/add-book', methods=['GET', 'POST'])
@admin_required
def add_book():
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        author_born_year = request.form.get('author_born_year')
        author_died_year = request.form.get('author_died_year')
        book_published_year = request.form.get('book_published_year')
        author_description = request.form.get('author_description')
        isbn = request.form.get('isbn')
        branch_category = request.form.get('branch_category')
        total_copies = int(request.form.get('total_copies', 1))
        
        # Convert year fields to integers (or None if empty)
        author_born_year = int(author_born_year) if author_born_year else None
        author_died_year = int(author_died_year) if author_died_year else None
        book_published_year = int(book_published_year) if book_published_year else None
        
        # Check if ISBN already exists
        existing_book = Book.query.filter_by(isbn=isbn).first()
        if existing_book:
            flash('A book with this ISBN already exists.', 'error')
            return redirect(url_for('add_book'))
        
        # Handle file upload
        cover_image = 'default_book.png'
        if 'cover' in request.files:
            file = request.files['cover']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(f"{isbn}_{file.filename}")
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                cover_image = filename
        
        new_book = Book(
            title=title,
            author=author,
            author_born_year=author_born_year,
            author_died_year=author_died_year,
            book_published_year=book_published_year,
            author_description=author_description,
            isbn=isbn,
            branch_category=branch_category,
            cover_image=cover_image,
            total_copies=total_copies,
            available_copies=total_copies
        )
        db.session.add(new_book)
        db.session.commit()
        flash('Book added successfully!', 'success')
        return redirect(url_for('add_book'))
    
    branches = ['Computer Science', 'Electronics', 'Mechanical', 'Civil', 'Electrical', 'General', 'Fiction', 'Science', 'Mathematics', 'History']
    return render_template('add_book.html', branches=branches)

@app.route('/admin/books')
@admin_required
def admin_books():
    books = Book.query.all()
    return render_template('admin_books.html', books=books)

@app.route('/admin/delete-book/<int:book_id>', methods=['POST'])
@admin_required
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    # Delete associated reservations and issued books
    Reservation.query.filter_by(book_id=book_id).delete()
    IssuedBook.query.filter_by(book_id=book_id).delete()
    db.session.delete(book)
    db.session.commit()
    flash('Book deleted successfully!', 'success')
    return redirect(url_for('admin_books'))

@app.route('/admin/edit-book/<int:book_id>', methods=['GET', 'POST'])
@admin_required
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)
    
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        author_born_year = request.form.get('author_born_year')
        author_died_year = request.form.get('author_died_year')
        book_published_year = request.form.get('book_published_year')
        author_description = request.form.get('author_description')
        isbn = request.form.get('isbn')
        branch_category = request.form.get('branch_category')
        total_copies = int(request.form.get('total_copies', 1))
        
        # Convert year fields to integers (or None if empty)
        author_born_year = int(author_born_year) if author_born_year else None
        author_died_year = int(author_died_year) if author_died_year else None
        book_published_year = int(book_published_year) if book_published_year else None
        
        # Check if ISBN already exists for a different book
        existing_book = Book.query.filter_by(isbn=isbn).first()
        if existing_book and existing_book.id != book_id:
            flash('A book with this ISBN already exists.', 'error')
            return redirect(url_for('edit_book', book_id=book_id))
        
        # Handle file upload
        cover_image = book.cover_image  # Keep existing cover by default
        if 'cover' in request.files:
            file = request.files['cover']
            if file and file.filename and allowed_file(file.filename):
                # Delete old cover if it's not the default
                if book.cover_image and book.cover_image != 'default_book.png':
                    try:
                        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], book.cover_image))
                    except:
                        pass
                
                # Save new cover
                filename = secure_filename(f"{isbn}_{file.filename}")
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                cover_image = filename
        
        # Update book details
        book.title = title
        book.author = author
        book.author_born_year = author_born_year
        book.author_died_year = author_died_year
        book.book_published_year = book_published_year
        book.author_description = author_description
        book.isbn = isbn
        book.branch_category = branch_category
        book.total_copies = total_copies
        book.cover_image = cover_image
        
        db.session.commit()
        flash('Book updated successfully!', 'success')
        return redirect(url_for('admin_books'))
    
    branches = ['Computer Science', 'Electronics', 'Mechanical', 'Civil', 'Electrical', 'General', 'Fiction', 'Science', 'Mathematics', 'History']
    return render_template('edit_book.html', book=book, branches=branches)

@app.route('/admin/students')
@admin_required
def admin_students():
    students = Student.query.all()
    return render_template('admin_students.html', students=students)

@app.route('/admin/delete_student/<int:student_id>', methods=['POST'])
@admin_required
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    
    # Safety check: Check if student has any borrowed books that haven't been returned
    active_issues = IssuedBook.query.filter_by(student_id=student_id, returned=False).count()
    
    if active_issues > 0:
        flash(f'Cannot delete student. {active_issues} book(s) must be returned first.', 'error')
        return redirect(url_for('admin_students'))
    
    # Delete associated reservations
    Reservation.query.filter_by(student_id=student_id).delete()
    
    # Delete all issued books (returned ones can be deleted as history)
    IssuedBook.query.filter_by(student_id=student_id).delete()
    
    # Delete renewal requests
    RenewalRequest.query.filter_by(student_id=student_id).delete()
    
    # Delete the student
    db.session.delete(student)
    db.session.commit()
    
    flash('Student deleted successfully!', 'success')
    return redirect(url_for('admin_students'))

@app.route('/admin/approvals')
@admin_required
def admin_approvals():
    pending = Reservation.query.filter_by(status='pending').all()
    approved = Reservation.query.filter_by(status='approved').order_by(Reservation.processed_date.desc()).limit(20).all()
    rejected = Reservation.query.filter_by(status='rejected').order_by(Reservation.processed_date.desc()).limit(20).all()
    return render_template('admin_approvals.html', pending=pending, approved=approved, rejected=rejected)

@app.route('/admin/approve/<int:reservation_id>', methods=['POST'])
@admin_required
def approve_reservation(reservation_id):
    reservation = Reservation.query.get_or_404(reservation_id)
    book = Book.query.get(reservation.book_id)
    
    if book.available_copies > 0:
        reservation.status = 'approved'
        reservation.processed_date = datetime.utcnow()
        
        # Create issued book record
        due_date = datetime.utcnow() + timedelta(days=7)  # 7 days borrowing period
        issued = IssuedBook(
            student_id=reservation.student_id,
            book_id=reservation.book_id,
            due_date=due_date
        )
        book.available_copies -= 1
        db.session.add(issued)
        db.session.commit()
        flash('Reservation approved and book issued!', 'success')
    else:
        flash('No copies available to issue.', 'error')
    
    return redirect(url_for('admin_approvals'))

@app.route('/admin/reject/<int:reservation_id>', methods=['POST'])
@admin_required
def reject_reservation(reservation_id):
    reservation = Reservation.query.get_or_404(reservation_id)
    reservation.status = 'rejected'
    reservation.processed_date = datetime.utcnow()
    db.session.commit()
    flash('Reservation rejected.', 'info')
    return redirect(url_for('admin_approvals'))

@app.route('/admin/issued-books')
@admin_required
def admin_issued_books():
    issued = IssuedBook.query.filter_by(returned=False).all()
    returned = IssuedBook.query.filter_by(returned=True).order_by(IssuedBook.return_date.desc()).limit(20).all()
    return render_template('admin_issued_books.html', issued=issued, returned=returned)

@app.route('/admin/return-book/<int:issue_id>', methods=['POST'])
@admin_required
def return_book(issue_id):
    issued = IssuedBook.query.get_or_404(issue_id)
    issued.returned = True
    issued.return_date = datetime.utcnow()
    
    book = Book.query.get(issued.book_id)
    book.available_copies += 1
    
    db.session.commit()
    flash('Book returned successfully!', 'success')
    return redirect(url_for('admin_issued_books'))

@app.route('/admin/renewals')
@admin_required
def admin_renewals():
    pending = RenewalRequest.query.filter_by(status='pending').all()
    approved = RenewalRequest.query.filter_by(status='approved').order_by(RenewalRequest.processed_date.desc()).limit(20).all()
    rejected = RenewalRequest.query.filter_by(status='rejected').order_by(RenewalRequest.processed_date.desc()).limit(20).all()
    return render_template('admin_renewals.html', pending=pending, approved=approved, rejected=rejected)

@app.route('/admin/approve-renewal/<int:renewal_id>', methods=['POST'])
@admin_required
def approve_renewal(renewal_id):
    renewal = RenewalRequest.query.get_or_404(renewal_id)
    issued_book = IssuedBook.query.get(renewal.issued_book_id)
    
    if issued_book and not issued_book.returned:
        renewal.status = 'approved'
        renewal.processed_date = datetime.utcnow()
        # Extend due date by 7 more days from current due date
        issued_book.due_date = issued_book.due_date + timedelta(days=7)
        db.session.commit()
        flash('Renewal approved! Due date extended by 7 days.', 'success')
    else:
        flash('Cannot approve renewal - book already returned or not found.', 'error')
    
    return redirect(url_for('admin_renewals'))

@app.route('/admin/reject-renewal/<int:renewal_id>', methods=['POST'])
@admin_required
def reject_renewal(renewal_id):
    renewal = RenewalRequest.query.get_or_404(renewal_id)
    renewal.status = 'rejected'
    renewal.processed_date = datetime.utcnow()
    db.session.commit()
    flash('Renewal request rejected.', 'info')
    return redirect(url_for('admin_renewals'))

# Student Routes
@app.route('/student/register', methods=['GET', 'POST'])
def student_register():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        branch = request.form.get('branch')
        register_number = request.form.get('register_number')
        phone_number = request.form.get('phone_number')
        password = request.form.get('password')
        
        # Check if register number already exists
        existing = Student.query.filter_by(register_number=register_number).first()
        if existing:
            flash('Register number already exists.', 'error')
            return redirect(url_for('student_register'))
        
        new_student = Student(
            full_name=full_name,
            branch=branch,
            register_number=register_number,
            phone_number=phone_number,
            password=generate_password_hash(password)
        )
        db.session.add(new_student)
        db.session.commit()
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('student_login'))
    
    branches = ['Computer Science', 'Mechanical', 'Mining', 'Electrical and Electronics', 'Mathematics', 'General']
    return render_template('student_register.html', branches=branches)

@app.route('/student/login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        register_number = request.form.get('register_number')
        password = request.form.get('password')
        
        student = Student.query.filter_by(register_number=register_number).first()
        if student and check_password_hash(student.password, password):
            session['student_id'] = student.id
            session['student_name'] = student.full_name
            flash('Login successful!', 'success')
            return redirect(url_for('student_dashboard'))
        flash('Invalid register number or password.', 'error')
    return render_template('student_login.html')

@app.route('/student/logout')
def student_logout():
    session.pop('student_id', None)
    session.pop('student_name', None)
    flash('Logged out successfully.', 'success')
    return redirect(url_for('index'))

@app.route('/student/dashboard')
@student_required
def student_dashboard():
    student = Student.query.get(session['student_id'])
    my_reservations = Reservation.query.filter_by(student_id=student.id).order_by(Reservation.request_date.desc()).all()
    my_issued = IssuedBook.query.filter_by(student_id=student.id, returned=False).all()
    my_renewals = RenewalRequest.query.filter_by(student_id=student.id).order_by(RenewalRequest.request_date.desc()).limit(10).all()
    return render_template('student_dashboard.html', student=student, reservations=my_reservations, issued_books=my_issued, renewal_requests=my_renewals)

@app.route('/student/renew/<int:issue_id>', methods=['POST'])
@student_required
def request_renewal(issue_id):
    issued = IssuedBook.query.get_or_404(issue_id)
    student_id = session['student_id']
    
    # Verify the book belongs to this student
    if issued.student_id != student_id:
        flash('Unauthorized request.', 'error')
        return redirect(url_for('student_dashboard'))
    
    # Check if there's already a pending renewal request
    existing = RenewalRequest.query.filter_by(
        issued_book_id=issue_id,
        status='pending'
    ).first()
    
    if existing:
        flash('You already have a pending renewal request for this book.', 'warning')
        return redirect(url_for('student_dashboard'))
    
    reason = request.form.get('reason', '').strip()
    if not reason:
        flash('Please provide a reason for renewal.', 'error')
        return redirect(url_for('student_dashboard'))
    
    renewal = RenewalRequest(
        issued_book_id=issue_id,
        student_id=student_id,
        reason=reason
    )
    db.session.add(renewal)
    db.session.commit()
    flash('Renewal request submitted successfully!', 'success')
    return redirect(url_for('student_dashboard'))

@app.route('/books')
def book_search():
    search = request.args.get('search', '')
    category = request.args.get('category', '')
    
    query = Book.query
    if search:
        query = query.filter(
            (Book.title.ilike(f'%{search}%')) |
            (Book.author.ilike(f'%{search}%')) |
            (Book.isbn.ilike(f'%{search}%'))
        )
    if category:
        query = query.filter_by(branch_category=category)
    
    books = query.all()
    # Fixed categories - always available regardless of books in database
    categories = ['Computer Science', 'Mechanical', 'Mining', 'Electrical and Electronics', 'Mathematics', 'General']
    
    return render_template('book_search.html', books=books, categories=categories, search=search, selected_category=category)

@app.route('/book/<int:book_id>')
def book_detail(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('book_detail.html', book=book)

@app.route('/reserve/<int:book_id>', methods=['POST'])
@student_required
def reserve_book(book_id):
    book = Book.query.get_or_404(book_id)
    student_id = session['student_id']
    
    # Check if student already has a pending reservation for this book
    existing = Reservation.query.filter_by(
        student_id=student_id,
        book_id=book_id,
        status='pending'
    ).first()
    
    if existing:
        flash('You already have a pending reservation for this book.', 'warning')
        return redirect(url_for('book_search'))
    
    # Check if student already has this book issued
    already_issued = IssuedBook.query.filter_by(
        student_id=student_id,
        book_id=book_id,
        returned=False
    ).first()
    
    if already_issued:
        flash('You already have this book issued.', 'warning')
        return redirect(url_for('book_search'))
    
    reservation = Reservation(
        student_id=student_id,
        book_id=book_id
    )
    db.session.add(reservation)
    db.session.commit()
    flash('Book reservation request submitted!', 'success')
    return redirect(url_for('student_dashboard'))

# API Routes for AJAX
@app.route('/api/book/isbn/<isbn>')
def get_book_by_isbn(isbn):
    book = Book.query.filter_by(isbn=isbn).first()
    if book:
        return jsonify({
            'found': True,
            'title': book.title,
            'author': book.author,
            'isbn': book.isbn,
            'branch_category': book.branch_category,
            'available': book.available_copies > 0
        })
    return jsonify({'found': False})

@app.route('/api/dashboard/stats')
@admin_required
def dashboard_stats():
    return jsonify({
        'total_books': Book.query.count(),
        'total_students': Student.query.count(),
        'pending_requests': Reservation.query.filter_by(status='pending').count(),
        'borrowed_books': IssuedBook.query.filter_by(returned=False).count()
    })

# REST API Endpoints for Mobile Application
@app.route('/api/login', methods=['POST'])
def api_login():
    """
    API endpoint for student login.
    Expects JSON: {"register_number": "...", "password": "..."}
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'success': False, 'message': 'No data provided'}), 400
    
    register_number = data.get('register_number')
    password = data.get('password')
    
    if not register_number or not password:
        return jsonify({'success': False, 'message': 'Register number and password are required'}), 400
    
    student = Student.query.filter_by(register_number=register_number).first()
    
    if student and check_password_hash(student.password, password):
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'student': {
                'id': student.id,
                'full_name': student.full_name,
                'branch': student.branch,
                'register_number': student.register_number,
                'phone_number': student.phone_number
            }
        }), 200
    else:
        return jsonify({'success': False, 'message': 'Invalid register number or password'}), 401

@app.route('/api/books', methods=['GET'])
def api_get_books():
    """
    API endpoint to get all books with complete information.
    Returns JSON array with all book details shown on the website.
    """
    books = Book.query.all()
    
    books_list = []
    for book in books:
        # Convert Book model to dictionary with all fields
        book_data = {
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'author_born_year': book.author_born_year,
            'author_died_year': book.author_died_year,
            'book_published_year': book.book_published_year,
            'author_description': book.author_description,
            'isbn': book.isbn,
            'branch_category': book.branch_category,
            'cover_image': book.cover_image,
            'total_copies': book.total_copies,
            'available_copies': book.available_copies,
            'created_at': book.created_at.strftime('%Y-%m-%d') if book.created_at else None
        }
        books_list.append(book_data)
    
    return jsonify(books_list), 200

@app.route('/api/book/<int:book_id>', methods=['GET'])
def api_get_book(book_id):
    """
    API endpoint to get details of a specific book.
    Returns JSON object with complete book information including author details.
    """
    book = Book.query.get_or_404(book_id)
    
    book_data = {
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'author_born_year': book.author_born_year,
        'author_died_year': book.author_died_year,
        'book_published_year': book.book_published_year,
        'author_description': book.author_description,
        'isbn': book.isbn,
        'category': book.branch_category,
        'cover_image': book.cover_image,
        'availability': 'Available' if book.available_copies > 0 else 'Not Available',
        'available_copies': book.available_copies,
        'total_copies': book.total_copies,
        'created_at': book.created_at.isoformat() if book.created_at else None
    }
    
    return jsonify({'success': True, 'book': book_data}), 200

@app.route('/api/reserve', methods=['POST'])
def api_reserve_book():
    """
    API endpoint to reserve a book.
    Expects JSON: {"student_id": ..., "book_id": ...}
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'success': False, 'message': 'No data provided'}), 400
    
    student_id = data.get('student_id')
    book_id = data.get('book_id')
    
    if not student_id or not book_id:
        return jsonify({'success': False, 'message': 'Student ID and Book ID are required'}), 400
    
    # Verify student exists
    student = Student.query.get(student_id)
    if not student:
        return jsonify({'success': False, 'message': 'Student not found'}), 404
    
    # Verify book exists
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'success': False, 'message': 'Book not found'}), 404
    
    # Check if student already has a pending reservation for this book
    existing_reservation = Reservation.query.filter_by(
        student_id=student_id,
        book_id=book_id,
        status='pending'
    ).first()
    
    if existing_reservation:
        return jsonify({'success': False, 'message': 'You already have a pending reservation for this book'}), 400
    
    # Check if student already has this book issued
    existing_issue = IssuedBook.query.filter_by(
        student_id=student_id,
        book_id=book_id,
        returned=False
    ).first()
    
    if existing_issue:
        return jsonify({'success': False, 'message': 'You already have this book issued'}), 400
    
    # Create reservation
    reservation = Reservation(
        student_id=student_id,
        book_id=book_id
    )
    db.session.add(reservation)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Book reservation request submitted successfully',
        'reservation_id': reservation.id
    }), 201

@app.route('/api/mybooks/<int:student_id>', methods=['GET'])
def api_get_student_books(student_id):
    """
    API endpoint to get all books reserved or borrowed by a student.
    Returns both reservations and issued books.
    """
    # Verify student exists
    student = Student.query.get(student_id)
    if not student:
        return jsonify({'success': False, 'message': 'Student not found'}), 404
    
    # Get all reservations for this student
    reservations = Reservation.query.filter_by(student_id=student_id).order_by(Reservation.request_date.desc()).all()
    
    # Get all issued books for this student (both returned and not returned)
    issued_books = IssuedBook.query.filter_by(student_id=student_id).all()
    
    reservations_list = []
    for reservation in reservations:
        book = Book.query.get(reservation.book_id)
        reservations_list.append({
            'type': 'reservation',
            'reservation_id': reservation.id,
            'book_id': book.id if book else None,
            'book_title': book.title if book else 'Unknown',
            'status': reservation.status,
            'request_date': reservation.request_date.isoformat() if reservation.request_date else None,
            'processed_date': reservation.processed_date.isoformat() if reservation.processed_date else None
        })
    
    issued_books_list = []
    for issued in issued_books:
        book = Book.query.get(issued.book_id)
        issued_books_list.append({
            'type': 'issued',
            'issue_id': issued.id,
            'book_id': book.id if book else None,
            'book_title': book.title if book else 'Unknown',
            'issue_date': issued.issue_date.isoformat() if issued.issue_date else None,
            'due_date': issued.due_date.isoformat() if issued.due_date else None,
            'return_date': issued.return_date.isoformat() if issued.return_date else None,
            'returned': issued.returned,
            'is_overdue': issued.is_overdue(),
            'days_overdue': issued.days_overdue(),
            'fine_amount': issued.calculate_fine()
        })
    
    return jsonify({
        'success': True,
        'student_id': student_id,
        'reservations': reservations_list,
        'issued_books': issued_books_list,
        'total_books': len(reservations_list) + len(issued_books_list)
    }), 200

# Initialize Database
def init_db():
    with app.app_context():
        db.create_all()
        # Create default admin if not exists
        if not Admin.query.filter_by(username='admin').first():
            admin = Admin(
                username='admin',
                password=generate_password_hash('admin123')
            )
            db.session.add(admin)
            db.session.commit()
            print("Default admin created: username='admin', password='admin123'")

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
