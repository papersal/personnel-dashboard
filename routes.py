from flask import render_template, request, redirect, flash, url_for, jsonify
from app import app, db
from models import Personnel, PLATFORM_POSITIONS, MAX_PERSONNEL_PER_POSITION
from datetime import datetime, date
from sqlalchemy import func


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name'].strip().title()
        platform = request.form['platform']
        position = request.form['position']
        joining_date = request.form['joining_date']

        # Validate inputs
        if not all([name, platform, position, joining_date]):
            flash("❌ All fields are required.", "error")
            return redirect('/')

        try:
            joining_dt = datetime.strptime(joining_date, "%Y-%m-%d").date()
            if joining_dt > date.today():
                flash("❌ Future date not allowed.", "error")
                return redirect('/')
        except ValueError:
            flash("❌ Invalid date format.", "error")
            return redirect('/')

        # Check if position exists for platform
        if platform not in PLATFORM_POSITIONS or position not in PLATFORM_POSITIONS[platform]:
            flash("❌ Invalid position for this platform.", "error")
            return redirect('/')

        # Check if position is full
        current_count = Personnel.query.filter_by(platform=platform, position=position).count()
        max_allowed = MAX_PERSONNEL_PER_POSITION.get(position, 1)
        
        if current_count >= max_allowed:
            flash(f"❌ Position {position} is full on {platform} ({current_count}/{max_allowed})", "error")
            return redirect('/')

        # Add new personnel
        new_personnel = Personnel(
            name=name,
            platform=platform,
            position=position,
            joining_date=joining_dt
        )
        
        db.session.add(new_personnel)
        db.session.commit()
        flash(f"✅ {name} added successfully.", "success")
        # Redirect back to admin if the request came from admin page
        if request.referrer and '/admin' in request.referrer:
            return redirect(url_for('admin'))
        return redirect('/')

    # Get all personnel for dashboard
    personnel = Personnel.query.order_by(Personnel.platform, Personnel.name).all()
    
    # Group by platform
    data = {}
    for person in personnel:
        if person.platform not in data:
            data[person.platform] = []
        data[person.platform].append(person)

    # Calculate vacant positions
    vacant = {}
    for platform, positions in PLATFORM_POSITIONS.items():
        vacant_positions = []
        for position in positions:
            current_count = Personnel.query.filter_by(platform=platform, position=position).count()
            max_allowed = MAX_PERSONNEL_PER_POSITION.get(position, 1)
            if current_count < max_allowed:
                vacant_positions.append(f"{position} ({max_allowed - current_count})")
        vacant[platform] = vacant_positions

    # Calculate stats
    total = len(personnel)
    platforms = len(data.keys())
    critical = len([p for p in personnel if p.days > 100])

    return render_template('dashboard.html', 
                         data=data, 
                         vacant=vacant,
                         total=total, 
                         platforms=platforms, 
                         critical=critical)


@app.route('/admin')
def admin():
    personnel = Personnel.query.order_by(Personnel.platform, Personnel.name).all()
    
    # Calculate statistics
    total = len(personnel)
    platforms = len(set(p.platform for p in personnel))
    critical = len([p for p in personnel if p.days > 100])
    
    # Platform status
    platform_status = []
    for platform, positions in PLATFORM_POSITIONS.items():
        total_positions = sum(MAX_PERSONNEL_PER_POSITION.get(pos, 1) for pos in positions)
        filled_positions = Personnel.query.filter_by(platform=platform).count()
        available_positions = total_positions - filled_positions
        percentage = (filled_positions / total_positions * 100) if total_positions > 0 else 0
        
        platform_status.append({
            'name': platform,
            'total_positions': total_positions,
            'filled_positions': filled_positions,
            'available_positions': available_positions,
            'percentage': percentage,
            'is_full': available_positions == 0
        })
    
    # Add today's date for the form
    from datetime import date
    today = date.today().strftime('%Y-%m-%d')
    
    return render_template('admin.html', 
                         personnel=personnel,
                         total=total,
                         platforms=platforms,
                         critical=critical,
                         platform_status=platform_status,
                         platform_positions=PLATFORM_POSITIONS,
                         today=today)


@app.route('/delete/<int:personnel_id>')
def delete_personnel(personnel_id):
    personnel = Personnel.query.get_or_404(personnel_id)
    name = personnel.name
    
    db.session.delete(personnel)
    db.session.commit()
    
    flash(f"✅ {name} removed successfully.", "success")
    return redirect(url_for('admin'))


@app.route('/api/positions/<platform>')
def get_positions(platform):
    """API endpoint to get available positions for a platform"""
    if platform not in PLATFORM_POSITIONS:
        return jsonify([])
    
    available_positions = []
    for position in PLATFORM_POSITIONS[platform]:
        current_count = Personnel.query.filter_by(platform=platform, position=position).count()
        max_allowed = MAX_PERSONNEL_PER_POSITION.get(position, 1)
        
        if current_count < max_allowed:
            available_positions.append({
                'position': position,
                'available': max_allowed - current_count,
                'total': max_allowed
            })
    
    return jsonify(available_positions)


@app.route('/tv')
def tv_dashboard():
    """TV Dashboard with slideshow view"""
    personnel = Personnel.query.order_by(Personnel.platform, Personnel.name).all()
    
    # Group personnel by platform
    platform_data = {}
    for person in personnel:
        if person.platform not in platform_data:
            platform_data[person.platform] = []
        platform_data[person.platform].append(person)
    
    # Split platforms into pages and separate rigs
    all_platforms = list(PLATFORM_POSITIONS.keys())
    platforms_page1 = {}
    platforms_page2 = {}
    all_rigs = {}
    
    non_rig_platforms = [p for p in all_platforms if not p.startswith('SAGAR')]
    rig_platforms = [p for p in all_platforms if p.startswith('SAGAR')]
    
    # Manually assign platforms to pages based on user preference
    page1_platforms = ['BHS', 'SCA', 'ICP', 'SHP', 'MHN', 'NQ', 'WIN', 'BPA']
    page2_platforms = ['BPB', 'B-193', 'TAPTI', 'PANNA', 'D1', 'NEELAM', 'HEERA', 'RATNA']
    
    for platform in page1_platforms:
        if platform in non_rig_platforms:
            platforms_page1[platform] = platform_data.get(platform, [])
    
    for platform in page2_platforms:
        if platform in non_rig_platforms:
            platforms_page2[platform] = platform_data.get(platform, [])
    
    # All rigs on separate slide
    for platform in rig_platforms:
        all_rigs[platform] = platform_data.get(platform, [])
    
    # Calculate shortages
    shortages = {}
    for platform, positions in PLATFORM_POSITIONS.items():
        missing_positions = []
        for position in positions:
            current_count = Personnel.query.filter_by(platform=platform, position=position).count()
            max_allowed = MAX_PERSONNEL_PER_POSITION.get(position, 1)
            if current_count < max_allowed:
                missing_positions.append(position)
        if missing_positions:
            shortages[platform] = missing_positions
    
    # Get critical personnel (>100 days)
    critical_people = [p for p in personnel if p.days > 100]
    
    # Calculate statistics
    total_personnel = len(personnel)
    active_platforms = len([p for p in platform_data.keys() if platform_data[p]])
    total_shortages = sum(len(positions) for positions in shortages.values())
    critical_personnel = len(critical_people)
    
    return render_template('tv_dashboard.html',
                         platforms_page1=platforms_page1,
                         platforms_page2=platforms_page2,
                         all_rigs=all_rigs,
                         shortages=shortages,
                         critical_people=critical_people,
                         total_personnel=total_personnel,
                         active_platforms=active_platforms,
                         total_shortages=total_shortages,
                         critical_personnel=critical_personnel)
