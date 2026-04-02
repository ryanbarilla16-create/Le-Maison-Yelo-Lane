from flask import render_template, request, redirect, url_for, flash, current_app, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Message
from models import db, User
import re
import random
import traceback
from datetime import datetime, date
from utils import get_ph_time
from .. import main_bp

# --- VALIDATION HELPERS ---
def has_repeated_chars(s, limit=4):
    if not s: return False
    return bool(re.search(r'(.)\1{' + str(limit - 1) + r',}', s))

def has_repeated_words(s):
    words = s.lower().split()
    return len(words) != len(set(words))

def validate_name(name, field_name):
    if not name: return True
    if len(name) > 50: return f"{field_name} must be 50 characters or less."
    if not re.match(r'^[A-Za-z\s\-]+$', name): return f"{field_name} can only contain letters, spaces, and dashes."
    if has_repeated_chars(name, 5): return f"{field_name} contains too many repeated characters."
    if has_repeated_words(name): return f"{field_name} cannot contain repeated words."
    return None

def validate_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(pattern, email): return "Please enter a valid email address."
    return None

def validate_username(username, first, last):
    if not (5 <= len(username) <= 20): return "Username must be 5-20 characters."
    if not re.match(r'^[A-Za-z0-9_]+$', username): return "Username can only contain letters, numbers, and underscores."
    if has_repeated_chars(username, 5): return "Username contains too many repeated characters."
    if username.lower() == first.lower() or username.lower() == last.lower():
        return "Username cannot be identical to your first or last name."
    return None

def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def validate_password(password, confirm):
    if len(password) < 6: return "Password must be at least 6 characters."
    if password.startswith(' ') or password.endswith(' '): return "Password cannot start or end with spaces."
    if '   ' in password: return "Password cannot contain too many consecutive spaces."
    if not re.search(r'[A-Z]', password): return "Password must contain an uppercase letter."
    if not re.search(r'[0-9]', password): return "Password must contain a number."
    if not re.search(r'[^A-Za-z0-9\s]', password): return "Password must contain a special character."
    if password != confirm: return "Passwords do not match."
    return None

@main_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form.get('first_name', '').strip()
        middle_name = request.form.get('middle_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        phone_number = request.form.get('phone_number', '').strip()
        birthday_str = request.form.get('birthday', '')
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        terms = request.form.get('terms')

        if not all([first_name, last_name, username, email, phone_number, birthday_str, password, confirm_password, terms]):
            flash("All required fields must be filled and terms accepted.", "danger")
            return render_template('auth/signup.html')

        for name, label in [(first_name, 'First Name'), (last_name, 'Last Name')]:
            err = validate_name(name, label)
            if err: flash(err, "danger"); return render_template('auth/signup.html')
        if middle_name:
            err = validate_name(middle_name, 'Middle Name')
            if err: flash(err, "danger"); return render_template('auth/signup.html')

        err = validate_email(email)
        if err: flash(err, "danger"); return render_template('auth/signup.html')

        err = validate_username(username, first_name, last_name)
        if err: flash(err, "danger"); return render_template('auth/signup.html')

        full_identity = f"{first_name} {last_name}".lower()
        if username.lower() == full_identity:
            flash("Username cannot be identical to Full Name.", "danger"); return render_template('auth/signup.html')

        try:
            birthday = datetime.strptime(birthday_str, '%Y-%m-%d').date()
            age = calculate_age(birthday)
            if age < 18:
                flash("You must be at least 18 years old to register.", "danger"); return render_template('auth/signup.html')
            if age > 70:
                flash("Please enter a valid birthday. Maximum age is 70 years.", "danger"); return render_template('auth/signup.html')
        except ValueError:
            flash("Invalid birthday format.", "danger"); return render_template('auth/signup.html')

        err = validate_password(password, confirm_password)
        if err: flash(err, "danger"); return render_template('auth/signup.html')

        if User.query.filter_by(email=email).first():
            flash("Email already registered.", "danger"); return render_template('auth/signup.html')
        if User.query.filter_by(username=username).first():
            flash("Username already taken.", "danger"); return render_template('auth/signup.html')
        if User.query.filter_by(first_name=first_name, last_name=last_name).first():
            flash("User with this First and Last name already exists.", "danger"); return render_template('auth/signup.html')

        new_user = User(
            first_name=first_name, middle_name=middle_name, last_name=last_name,
            username=username, email=email, phone_number=phone_number, birthday=birthday, status='PENDING'
        )
        new_user.set_password(password)
        
        otp = f"{random.randint(100000, 999999)}"
        new_user.otp_code = otp
        new_user.otp_created_at = get_ph_time()
        new_user.is_verified = False

        db.session.add(new_user)
        db.session.commit()

        print(f"--- OTP FOR {email} IS: {otp} ---")
        
        # Send OTP via Gmail
        try:
            mail = current_app.extensions['mail']
            msg = Message(
                subject='Le Maison Yelo Lane - Your OTP Verification Code',
                sender=current_app.config['MAIL_USERNAME'],
                recipients=[email]
            )
            msg.html = f"""
            <div style="font-family: 'Georgia', serif; max-width: 500px; margin: 0 auto; padding: 40px 30px; background: #ffffff; border-radius: 12px; border: 1px solid #e0d5c7;">
                <div style="text-align: center; margin-bottom: 30px;">
                    <h1 style="color: #8B4513; margin: 0; font-size: 1.5rem;">☕ Le Maison Yelo Lane</h1>
                    <p style="color: #999; font-size: 0.85rem; margin-top: 5px;">Email Verification</p>
                </div>
                <p style="color: #333; font-size: 1rem;">Hello <strong>{first_name}</strong>,</p>
                <p style="color: #555; font-size: 0.95rem;">Thank you for registering! Please use the following OTP code to verify your email address:</p>
                <div style="text-align: center; margin: 30px 0;">
                    <span style="display: inline-block; background: linear-gradient(135deg, #8B4513, #A0522D); color: #fff; font-size: 2rem; font-weight: bold; letter-spacing: 8px; padding: 15px 35px; border-radius: 10px;">{otp}</span>
                </div>
                <p style="color: #999; font-size: 0.8rem; text-align: center;">This code will expire in 10 minutes. Do not share it with anyone.</p>
                <hr style="border: none; border-top: 1px solid #e0d5c7; margin: 25px 0;">
                <p style="color: #bbb; font-size: 0.75rem; text-align: center;">If you did not request this, please ignore this email.</p>
            </div>
            """
            mail.send(msg)
            flash(f"An OTP has been sent to {email}. Please check your inbox.", "success")
        except Exception as e:
            print(f"Email sending failed: {e}")
            traceback.print_exc()
            flash(f"An OTP has been generated. (Email sending failed, check console for OTP)", "warning")
        
        return redirect(url_for('main.verify_otp', user_id=new_user.id))

    return render_template('auth/signup.html')


@main_bp.route('/verify_otp/<int:user_id>', methods=['GET', 'POST'])
def verify_otp(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        otp_input = request.form.get('otp', '').strip()
        if user.otp_code == otp_input:
            user.is_verified = True
            user.otp_code = None
            db.session.commit()
            flash("Account successfully verified! Please wait for admin approval.", "success")
            return redirect(url_for('main.login'))
        else:
            flash("Invalid OTP.", "danger")
    
    # Calculate remaining cooldown seconds for the resend button
    cooldown_remaining = 0
    if user.otp_created_at:
        elapsed = (get_ph_time() - user.otp_created_at).total_seconds()
        cooldown_remaining = max(0, int(300 - elapsed))  # 300 seconds = 5 minutes
    
    return render_template('auth/verify_otp.html', user=user, cooldown_remaining=cooldown_remaining)

@main_bp.route('/resend_otp/<int:user_id>', methods=['POST'])
def resend_otp(user_id):
    user = User.query.get_or_404(user_id)
    
    if user.is_verified:
        flash("Your account is already verified.", "info")
        return redirect(url_for('main.login'))
    
    # 5-minute cooldown check
    if user.otp_created_at:
        elapsed = (get_ph_time() - user.otp_created_at).total_seconds()
        if elapsed < 300:  # 300 seconds = 5 minutes
            remaining = int(300 - elapsed)
            minutes = remaining // 60
            seconds = remaining % 60
            flash(f"Please wait {minutes}m {seconds}s before requesting a new code.", "warning")
            return redirect(url_for('main.verify_otp', user_id=user.id))
    
    # Generate a new OTP
    otp = f"{random.randint(100000, 999999)}"
    user.otp_code = otp
    user.otp_created_at = get_ph_time()
    db.session.commit()
    
    print(f"--- RESEND OTP FOR {user.email} IS: {otp} ---")
    
    # Send OTP via Gmail
    try:
        mail = current_app.extensions['mail']
        msg = Message(
            subject='Le Maison Yelo Lane - Your New OTP Code',
            sender=current_app.config['MAIL_USERNAME'],
            recipients=[user.email]
        )
        msg.html = f"""
        <div style="font-family: 'Georgia', serif; max-width: 500px; margin: 0 auto; padding: 40px 30px; background: #ffffff; border-radius: 12px; border: 1px solid #e0d5c7;">
            <div style="text-align: center; margin-bottom: 30px;">
                <h1 style="color: #8B4513; margin: 0; font-size: 1.5rem;">☕ Le Maison Yelo Lane</h1>
                <p style="color: #999; font-size: 0.85rem; margin-top: 5px;">New Verification Code</p>
            </div>
            <p style="color: #333; font-size: 1rem;">Hello <strong>{user.first_name}</strong>,</p>
            <p style="color: #555; font-size: 0.95rem;">Here is your new OTP verification code:</p>
            <div style="text-align: center; margin: 30px 0;">
                <span style="display: inline-block; background: linear-gradient(135deg, #8B4513, #A0522D); color: #fff; font-size: 2rem; font-weight: bold; letter-spacing: 8px; padding: 15px 35px; border-radius: 10px;">{otp}</span>
            </div>
            <p style="color: #999; font-size: 0.8rem; text-align: center;">This code will expire in 10 minutes. Do not share it with anyone.</p>
            <hr style="border: none; border-top: 1px solid #e0d5c7; margin: 25px 0;">
            <p style="color: #bbb; font-size: 0.75rem; text-align: center;">If you did not request this, please ignore this email.</p>
        </div>
        """
        mail.send(msg)
        flash(f"A new OTP has been sent to {user.email}. Please check your inbox.", "success")
    except Exception as e:
        print(f"Email sending failed: {e}")
        traceback.print_exc()
        flash(f"A new OTP has been generated. (Email sending failed, check console for OTP)", "warning")
    
    return redirect(url_for('main.verify_otp', user_id=user.id))

@main_bp.route('/social_auth', methods=['POST'])
def social_auth():
    import secrets
    from werkzeug.security import generate_password_hash
    
    data = request.json
    if not data:
        return jsonify({"success": False, "message": "No data provided"}), 400
        
    email = data.get('email')
    first_name = data.get('first_name', '')
    last_name = data.get('last_name', '')
    provider = data.get('provider')
    picture_url = data.get('picture_url')
    
    if not email:
        return jsonify({"success": False, "message": "Email is required from social provider"}), 400
        
    user = User.query.filter_by(email=email).first()
    
    if user:
        if picture_url and not user.profile_picture_url:
            user.profile_picture_url = picture_url
            db.session.commit()
            
        if user.status != 'ACTIVE' and user.role not in ['ADMIN', 'CASHIER', 'INVENTORY_STAFF']:
            flash(f"Your {provider} login was successful, but your account is pending admin approval.", "warning")
            return jsonify({"success": True, "redirect": url_for('main.login')})
            
        login_user(user)
        
        if user.role == 'CASHIER':
            redir_url = url_for('admin.orders')
        elif user.role == 'INVENTORY_STAFF':
            redir_url = url_for('admin.inventory')
        elif user.role == 'ADMIN':
            redir_url = url_for('admin.overview')
        else:
            redir_url = url_for('main.index')
            
        return jsonify({"success": True, "redirect": redir_url})
    
    # Auto-create user since they used social login
    base_username = (first_name + last_name).lower().replace(' ', '')
    username = f"{base_username}{secrets.randbelow(9999)}"
    
    # Ensure unique username
    while User.query.filter_by(username=username).first():
        username = f"{base_username}{secrets.randbelow(99999)}"
        
    random_password = secrets.token_urlsafe(16)
    
    new_user = User(
        first_name=first_name, 
        last_name=last_name,
        username=username, 
        email=email, 
        status='PENDING',
        is_verified=True,
        profile_picture_url=picture_url
    )
    new_user.set_password(random_password)
    
    db.session.add(new_user)
    db.session.commit()
    
    flash(f"Welcome {first_name}! Your account was created via {provider} but requires admin approval before you can log in.", "success")
    return jsonify({
        "success": True, 
        "redirect": url_for('main.login')
    })

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        pwd = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(pwd):
            if not user.is_verified:
                flash("Please complete your OTP verification first.", "warning")
                return redirect(url_for('main.verify_otp', user_id=user.id))
            
            role_upper = user.role.upper() if user.role else ''
            staff_roles = ['ADMIN', 'CASHIER', 'INVENTORY_STAFF', 'INVENTORY', 'KITCHEN', 'STAFF', 'RIDER']
            
            if user.status != 'ACTIVE' and role_upper not in staff_roles:
                flash("Your account is pending admin approval.", "warning")
                return redirect(url_for('main.login'))
            
            login_user(user)
            # Redirect admins/staff to their specific dashboards, regular users to homepage
            if role_upper == 'ADMIN':
                return redirect(url_for('admin.overview'))
            elif role_upper in ['CASHIER', 'STAFF']:
                return redirect(url_for('admin.orders'))
            elif role_upper in ['INVENTORY_STAFF', 'INVENTORY']:
                return redirect(url_for('admin.inventory'))
            elif role_upper == 'KITCHEN':
                return redirect(url_for('admin.kitchen_view'))
            elif role_upper == 'RIDER':
                return redirect(url_for('admin.deliveries'))
                
            return redirect(url_for('main.index'))
        flash("Invalid email or password.", "danger")
    return render_template('auth/login.html')

@main_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    from flask import session
    if request.method == 'POST':
        email = (request.form.get('email') or '').strip()
        user = User.query.filter_by(email=email).first()
        
        if not user:
            # Reveal as little as possible
            flash(f"If an account exists for {email}, an OTP has been sent.", "info")
            return redirect(url_for('main.login'))
            
        # Rate-limit OTP (wait 60 seconds between requests)
        if user.otp_created_at:
            elapsed = (get_ph_time() - user.otp_created_at).total_seconds()
            if elapsed < 60:
                flash(f"Please wait {int(60 - elapsed)}s before requesting a new code.", "warning")
                return redirect(url_for('main.verify_reset_otp', user_id=user.id))
        
        otp = f"{random.randint(100000, 999999)}"
        user.otp_code = otp
        user.otp_created_at = get_ph_time()
        db.session.commit()
        
        print(f"--- WEB FORGOT PASSWORD OTP FOR {email} IS: {otp} ---")
        
        try:
            mail = current_app.extensions['mail']
            msg = Message(
                subject='Le Maison Yelo Lane - Password Reset Code',
                sender=current_app.config['MAIL_USERNAME'],
                recipients=[email]
            )
            msg.html = f"""
            <div style="font-family: 'Georgia', serif; max-width: 500px; margin: 0 auto; padding: 40px 30px; background: #ffffff; border-radius: 12px; border: 1px solid #e0d5c7;">
                <div style="text-align: center; margin-bottom: 30px;">
                    <h1 style="color: #8B4513; margin: 0; font-size: 1.5rem;">Le Maison Yelo Lane</h1>
                    <p style="color: #999; font-size: 0.85rem; margin-top: 5px;">Password Reset</p>
                </div>
                <p style="color: #333;">Hello <strong>{user.first_name}</strong>,</p>
                <p style="color: #555;">You requested a password reset. Use the following OTP code to reset your password:</p>
                <div style="text-align: center; margin: 30px 0;">
                    <span style="display: inline-block; background: linear-gradient(135deg, #8B4513, #A0522D); color: #fff; font-size: 2rem; font-weight: bold; letter-spacing: 8px; padding: 15px 35px; border-radius: 10px;">{otp}</span>
                </div>
                <p style="color: #999; font-size: 0.8rem; text-align: center;">This code will expire in 5 minutes. If you didn't request this, please ignore this email.</p>
            </div>
            """
            mail.send(msg)
            flash(f"An OTP has been sent to {email}. Please check your inbox.", "success")
        except Exception as e:
            print(f"Email sending failed: {e}")
            traceback.print_exc()
            flash("An OTP has been generated. (Email sending failed, check console for OTP)", "warning")
            
        session['reset_user_id'] = user.id
        return redirect(url_for('main.verify_reset_otp', user_id=user.id))
        
    return render_template('auth/forgot_password.html')

@main_bp.route('/verify-reset-otp/<int:user_id>', methods=['GET', 'POST'])
def verify_reset_otp(user_id):
    from flask import session
    if session.get('reset_user_id') != user_id:
        flash("Invalid session. Please start the password reset process again.", "danger")
        return redirect(url_for('main.forgot_password'))
        
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        otp_input = request.form.get('otp', '').strip()
        
        # Check OTP expiry (5 minutes)
        if user.otp_created_at:
            elapsed = (get_ph_time() - user.otp_created_at).total_seconds()
            if elapsed > 300:
                flash("OTP has expired. Please request a new one.", "danger")
                return redirect(url_for('main.verify_reset_otp', user_id=user.id))
                
        if user.otp_code == otp_input:
            session['reset_verified_user_id'] = user.id
            flash("OTP verified! You can now set a new password.", "success")
            return redirect(url_for('main.reset_password'))
        else:
            flash("Invalid OTP.", "danger")
            
    cooldown_remaining = 0
    if user.otp_created_at:
        elapsed = (get_ph_time() - user.otp_created_at).total_seconds()
        cooldown_remaining = max(0, int(60 - elapsed))
        
    return render_template('auth/verify_reset_otp.html', user=user, cooldown_remaining=cooldown_remaining)

@main_bp.route('/resend-reset-otp/<int:user_id>', methods=['POST'])
def resend_reset_otp(user_id):
    from flask import session
    if session.get('reset_user_id') != user_id:
        flash("Invalid session. Please start the password reset process again.", "danger")
        return redirect(url_for('main.forgot_password'))
        
    user = User.query.get_or_404(user_id)
    
    if user.otp_created_at:
        elapsed = (get_ph_time() - user.otp_created_at).total_seconds()
        if elapsed < 60:
            remaining = int(60 - elapsed)
            flash(f"Please wait {remaining}s before requesting a new code.", "warning")
            return redirect(url_for('main.verify_reset_otp', user_id=user.id))
            
    otp = f"{random.randint(100000, 999999)}"
    user.otp_code = otp
    user.otp_created_at = get_ph_time()
    db.session.commit()
    
    print(f"--- WEB RESEND FORGOT PASSWORD OTP FOR {user.email} IS: {otp} ---")
    
    try:
        mail = current_app.extensions['mail']
        msg = Message(
            subject='Le Maison Yelo Lane - New Password Reset Code',
            sender=current_app.config['MAIL_USERNAME'],
            recipients=[user.email]
        )
        msg.html = f"""
        <div style="font-family: 'Georgia', serif; max-width: 500px; margin: 0 auto; padding: 40px 30px; background: #ffffff; border-radius: 12px; border: 1px solid #e0d5c7;">
            <div style="text-align: center; margin-bottom: 30px;">
                <h1 style="color: #8B4513; margin: 0; font-size: 1.5rem;">Le Maison Yelo Lane</h1>
                <p style="color: #999; font-size: 0.85rem; margin-top: 5px;">New Password Reset Code</p>
            </div>
            <p style="color: #333;">Hello <strong>{user.first_name}</strong>,</p>
            <p style="color: #555;">Here is your new OTP code to reset your password:</p>
            <div style="text-align: center; margin: 30px 0;">
                <span style="display: inline-block; background: linear-gradient(135deg, #8B4513, #A0522D); color: #fff; font-size: 2rem; font-weight: bold; letter-spacing: 8px; padding: 15px 35px; border-radius: 10px;">{otp}</span>
            </div>
            <p style="color: #999; font-size: 0.8rem; text-align: center;">This code will expire in 5 minutes. If you didn't request this, please ignore this email.</p>
        </div>
        """
        mail.send(msg)
        flash(f"A new OTP has been sent to {user.email}. Please check your inbox.", "success")
    except Exception as e:
        print(f"Email sending failed: {e}")
        traceback.print_exc()
        flash("A new OTP has been generated. (Email sending failed, check console for OTP)", "warning")
        
    return redirect(url_for('main.verify_reset_otp', user_id=user.id))

@main_bp.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    from flask import session
    user_id = session.get('reset_verified_user_id')
    if not user_id:
        flash("You must verify your OTP before resetting your password.", "danger")
        return redirect(url_for('main.forgot_password'))
        
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Check OTP expiry (5 minutes) - extra safety
        if user.otp_created_at:
            elapsed = (get_ph_time() - user.otp_created_at).total_seconds()
            if elapsed > 300:
                flash("Your password reset session has expired (5 minutes). Please start over.", "danger")
                session.pop('reset_user_id', None)
                session.pop('reset_verified_user_id', None)
                return redirect(url_for('main.forgot_password'))
                
        err = validate_password(new_password, confirm_password)
        if err:
            flash(err, "danger")
            return render_template('auth/reset_password.html')
            
        user.set_password(new_password)
        user.otp_code = None
        user.otp_created_at = None
        db.session.commit()
        
        # Send system notification on the new password change
        from utils import create_notification
        create_notification(user.id, 'Password Changed', 'Your password was successfully changed.', 'SYSTEM')
        
        session.pop('reset_user_id', None)
        session.pop('reset_verified_user_id', None)
        
        flash("Password reset successfully! You can now log in with your new password.", "success")
        return redirect(url_for('main.login'))
        
    return render_template('auth/reset_password.html')

@main_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        phone_number = request.form.get('phone_number', '').strip()

        # Simple validations
        if not all([first_name, last_name, username, email, phone_number]):
            flash("All fields are required.", "danger")
            return redirect(url_for('main.profile'))

        # Check for username / email conflicts if they changed it
        if email != current_user.email:
            existing = User.query.filter_by(email=email).first()
            if existing:
                flash("Email already registered by another account.", "danger")
                return redirect(url_for('main.profile'))
                
        if username != current_user.username:
            existing = User.query.filter_by(username=username).first()
            if existing:
                flash("Username already taken.", "danger")
                return redirect(url_for('main.profile'))

        current_user.first_name = first_name
        current_user.last_name = last_name
        current_user.username = username
        current_user.email = email
        current_user.phone_number = phone_number

        import os
        from werkzeug.utils import secure_filename
        from flask import current_app

        profile_picture = request.files.get('profile_picture')
        if profile_picture and profile_picture.filename:
            # Ensure folder exists
            upload_folder = os.path.join(current_app.root_path, 'static', 'uploads', 'profiles')
            os.makedirs(upload_folder, exist_ok=True)
            
            filename = secure_filename(f"{current_user.id}_{profile_picture.filename}")
            filepath = os.path.join(upload_folder, filename)
            profile_picture.save(filepath)
            
            # Update user model with relative URL for frontend
            current_user.profile_picture_url = url_for('static', filename=f"uploads/profiles/{filename}")

        db.session.commit()
        flash("Profile updated successfully.", "success")
        return redirect(url_for('main.profile'))

    return render_template('auth/profile.html')

@main_bp.route('/mobile/social')
def mobile_social():
    import os
    provider = request.args.get('provider')
    session_id = request.args.get('session_id')
    
    # For Facebook, use server-side OAuth redirect (no popup needed)
    if provider == 'facebook':
        fb_app_id = os.environ.get('FACEBOOK_APP_ID', '')
        # Force https because Localtunnel uses it and Facebook requires it
        redirect_uri = f"https://{request.host}/auth/facebook/callback"
        fb_oauth_url = (
            f"https://www.facebook.com/v18.0/dialog/oauth"
            f"?client_id={fb_app_id}"
            f"&redirect_uri={redirect_uri}"
            f"&scope=email,public_profile"
            f"&state={session_id}"
        )
        return redirect(fb_oauth_url)
    
    # For Google (or other providers), render the JS page
    facebook_app_id = os.environ.get('FACEBOOK_APP_ID', '')
    google_client_id = os.environ.get('GOOGLE_CLIENT_ID', '')
    return render_template('auth/mobile_social.html',
                           provider=provider,
                           session_id=session_id,
                           FACEBOOK_APP_ID=facebook_app_id,
                           GOOGLE_CLIENT_ID=google_client_id)


@main_bp.route('/auth/facebook/callback')
def facebook_callback():
    import os, requests as ext_requests
    code = request.args.get('code')
    session_id = request.args.get('state', '')
    
    if not code:
        return '<h2>Login cancelled.</h2><p>You can close this window.</p>'
    
    fb_app_id = os.environ.get('FACEBOOK_APP_ID', '')
    fb_app_secret = os.environ.get('FACEBOOK_APP_SECRET', '')
    # Force https because Localtunnel uses it and Facebook requires it
    redirect_uri = f"https://{request.host}/auth/facebook/callback"
    
    # Exchange code for access token
    token_url = (
        f"https://graph.facebook.com/v18.0/oauth/access_token"
        f"?client_id={fb_app_id}"
        f"&redirect_uri={redirect_uri}"
        f"&client_secret={fb_app_secret}"
        f"&code={code}"
    )
    token_res = ext_requests.get(token_url).json()
    access_token = token_res.get('access_token')
    
    if not access_token:
        # If the code was already used, the session might already have the data
        # This happens when mobile browsers retry the callback
        from routes.api import mobile_sessions
        if session_id and session_id in mobile_sessions and mobile_sessions[session_id].get('success'):
            return '''
            <html><body style="font-family:sans-serif;text-align:center;padding:40px;">
            <h2 style="color:#8B4513;">✅ Login Successful!</h2>
            <p>You can now go back to the app.</p>
            <p style="color:#666;font-size:14px;">This window will close automatically...</p>
            </body></html>
            '''
        # Check if error is "code already used" - still show success-like page
        error_msg = str(token_res)
        if 'has been used' in error_msg:
            return '''
            <html><body style="font-family:sans-serif;text-align:center;padding:40px;">
            <h2 style="color:#8B4513;">✅ Login Successful!</h2>
            <p>You can now go back to the app.</p>
            <p style="color:#666;font-size:14px;">This window will close automatically...</p>
            </body></html>
            '''
        return f'<h2>Authentication failed.</h2><p>Could not get access token.</p><p>{error_msg}</p>'
    
    # Get user info
    user_url = f"https://graph.facebook.com/me?fields=id,name,email,first_name,last_name,picture.type(large)&access_token={access_token}"
    user_data = ext_requests.get(user_url).json()
    
    email = user_data.get('email')
    first_name = user_data.get('first_name', '')
    last_name = user_data.get('last_name', '')
    picture_url = None
    if user_data.get('picture', {}).get('data', {}).get('url'):
        picture_url = user_data['picture']['data']['url']
    
    # Store result for polling (reuse existing complete endpoint logic)
    from routes.api import mobile_sessions
    mobile_sessions[session_id] = {
        'success': True,
        'provider': 'Facebook',
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
        'picture_url': picture_url
    }
    
    # Also do the actual login/signup
    from models import User
    user = User.query.filter_by(email=email).first()
    if user:
        mobile_sessions[session_id]['user'] = {
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'role': user.role
        }
    else:
        # Create new user
        import secrets
        new_user = User(
            email=email,
            first_name=first_name,
            last_name=last_name,
            username=email.split('@')[0],
            is_verified=True,
            social_provider='Facebook'
        )
        new_user.set_password(secrets.token_hex(16))
        from extensions import db
        db.session.add(new_user)
        db.session.commit()
        mobile_sessions[session_id]['user'] = {
            'id': new_user.id,
            'email': new_user.email,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'username': new_user.username,
            'role': new_user.role
        }
    
    return '''
    <html><body style="font-family:sans-serif;text-align:center;padding:40px;">
    <h2 style="color:#8B4513;">✅ Login Successful!</h2>
    <p>You can now go back to the app.</p>
    <p style="color:#666;font-size:14px;">This window will close automatically...</p>
    </body></html>
    '''
