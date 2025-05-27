from flask import Blueprint, request, jsonify
from .models import PhoneNumbers, Jobs, Sections, PhoneTypes,Users
from . import db
api_blueprint = Blueprint('api', __name__)
from sqlalchemy.exc import IntegrityError
from flask import request, jsonify
from sqlalchemy import or_


# ----------------------------------phonenumbers --------------------------------
#=========================================post========================
@api_blueprint.route('/api/phones/add/phonenumber', methods=['POST'])
def add_phonenumber():
    data = request.get_json()
    if not all(key in data for key in ['JobID', 'PhoneNumber']):
        return jsonify({"error": "Missing required fields: JobID, PhoneNumber"}), 400

    try:
        # Check if JobID exists
        job = Jobs.query.get(data['JobID'])
        if not job:
            return jsonify({"error": "Invalid JobID"}), 400

        # Check phone number count for the job
        phone_count = PhoneNumbers.query.filter_by(JobID=data['JobID']).count()
        if phone_count >= 3:
            return jsonify({"error": "Maximum 3 phone numbers allowed per job"}), 400

        # Validate PhoneTypeID if provided
        if 'PhoneTypeID' in data and data['PhoneTypeID']:
            phone_type = PhoneTypes.query.get(data['PhoneTypeID'])
            if not phone_type:
                return jsonify({"error": "Invalid PhoneTypeID"}), 400

        phonenumber = PhoneNumbers(
            JobID=data['JobID'],
            PhoneNumber=data['PhoneNumber'],
            PhoneTypeID=data.get('PhoneTypeID')
        )
        db.session.add(phonenumber)
        db.session.commit()
        return jsonify({
            "PhoneID": phonenumber.PhoneID,
            "JobID": phonenumber.JobID,
            "PhoneNumber": phonenumber.PhoneNumber,
            "PhoneTypeID": phonenumber.PhoneTypeID,
            "message": "Phone number created"
        }), 201
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": "Database constraint violation (e.g., duplicate phone number)"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

#=========================================GET ALL========================
@api_blueprint.route('/api/phones/phonenumbers', methods=['GET'])
def get_phonenumbers():
    try:
        phonenumbers = PhoneNumbers.query.join(PhoneTypes, isouter=True).all()
        result = []
        for phone in phonenumbers:
            job = Jobs.query.get(phone.JobID)
            section = Sections.query.get(job.SectionID) if job else None

            result.append({
                "PhoneID": phone.PhoneID,
                "JobID": phone.JobID,
                "PhoneNumber": phone.PhoneNumber,
                "PhoneTypeName": phone.phone_type.PhoneTypeName if phone.phone_type else None,
                "JobTitle": job.JobTitle if job else "Unknown Job",
                "SectionName": section.SectionName if section else "Unknown Section"
            })
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# =========================================GET PHONEID================================
@api_blueprint.route('/api/phones/<int:phone_id>', methods=['GET'])
def get_phonenumber(phone_id):
    try:
        phone = (
            PhoneNumbers.query
            .join(PhoneTypes, PhoneNumbers.PhoneTypeID == PhoneTypes.PhoneTypeID, isouter=True)
            .filter(PhoneNumbers.PhoneID == phone_id)
            .first()
        )

        if not phone:
            return jsonify({"error": "Phone number not found"}), 404

        return jsonify({
            "PhoneID": phone.PhoneID,
            "JobID": phone.JobID,
            "PhoneNumber": phone.PhoneNumber,
            "PhoneTypeName": phone.phone_type.PhoneTypeName if phone.phone_type else None
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500




#=========================================UPDATE PHONEID========================
@api_blueprint.route('/api/phones/<int:phone_id>', methods=['PUT'])
def update_phonenumber(phone_id):
    data = request.get_json()
    try:
        phone = PhoneNumbers.query.get(phone_id)
        if not phone:
            return jsonify({"error": "Phone number not found"}), 404

        if 'JobID' in data:
            job = Jobs.query.get(data['JobID'])
            if not job:
                return jsonify({"error": "Invalid JobID"}), 400
            phone.JobID = data['JobID']

        if 'PhoneNumber' in data:
            phone.PhoneNumber = data['PhoneNumber']

        if 'PhoneTypeID' in data:
            if data['PhoneTypeID']:
                phone_type = PhoneTypes.query.get(data['PhoneTypeID'])
                if not phone_type:
                    return jsonify({"error": "Invalid PhoneTypeID"}), 400
            phone.PhoneTypeID = data['PhoneTypeID']

        db.session.commit()
        return jsonify({
            "PhoneID": phone.PhoneID,
            "JobID": phone.JobID,
            "PhoneNumber": phone.PhoneNumber,
            "PhoneTypeID": phone.PhoneTypeID,
            "message": "Phone number updated"
        })
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": "Database constraint violation"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

#=========================================DELETE PHONEID========================
@api_blueprint.route('/api/phones/<int:phone_id>', methods=['DELETE'])
def delete_phonenumber(phone_id):
    try:
        phone = PhoneNumbers.query.get(phone_id)
        if not phone:
            return jsonify({"error": "Phone number not found"}), 404
        db.session.delete(phone)
        db.session.commit()
        return jsonify({"message": "Phone number deleted"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# -----------------------------------------------SECTIONS-----------------------------------------------
#=================================================GET ALL SECTIONS================================
@api_blueprint.route('/api/sections', methods=['GET'])
def get_sections():
    try:
        sections = Sections.query.all()
        return jsonify([{
            "SectionID": section.SectionID,
            "SectionName": section.SectionName,
            "Description": section.Description
        } for section in sections])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#=================================================GET SINGLE SECTIONS================================
@api_blueprint.route('/api/sections/<int:section_id>', methods=['GET'])
def get_section(section_id):
    try:
        section = Sections.query.get(section_id)
        if not section:
            return jsonify({"error": "Section not found"}), 404
        return jsonify({
            "SectionID": section.SectionID,
            "SectionName": section.SectionName,
            "Description": section.Description
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =================================POST SECTION===================================
@api_blueprint.route('/api/sections', methods=['POST'])
def add_section():
    data = request.get_json()
    if not all(key in data for key in ['SectionName']):
        return jsonify({"error": "Missing required field: SectionName"}), 400

    try:
        section = Sections(
            SectionName=data['SectionName'],
            Description=data.get('Description')
        )
        db.session.add(section)
        db.session.commit()
        return jsonify({
            "SectionID": section.SectionID,
            "message": "Section created"
        }), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "SectionName must be unique"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ==============================UPDATE SECTION ID
@api_blueprint.route('/api/sections/<int:section_id>', methods=['PUT'])
def update_section(section_id):
    data = request.get_json()
    try:
        section = Sections.query.get(section_id)
        if not section:
            return jsonify({"error": "Section not found"}), 404

        if 'SectionName' in data:
            section.SectionName = data['SectionName']
        if 'Description' in data:
            section.Description = data['Description']

        db.session.commit()
        return jsonify({
            "SectionID": section.SectionID,
            "message": "Section updated"
        })
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "SectionName must be unique"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500



# ================================DELETE SECTION ID
@api_blueprint.route('/api/sections/<int:section_id>', methods=['DELETE'])
def delete_section(section_id):
    try:
        section = Sections.query.get(section_id)
        if not section:
            return jsonify({"error": "Section not found"}), 404
        db.session.delete(section)
        db.session.commit()
        return jsonify({"message": "Section deleted"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500



#-----------------------------------------------PHONETYPES----------------------------
# =========================================GET ALL PHONE TYPES=========================
@api_blueprint.route('/api/phonetypes', methods=['GET'])
def get_phonetypes():
    try:
        phonetypes = PhoneTypes.query.all()
        return jsonify([
            {
                "phoneTypeId": pt.PhoneTypeID,
                "phoneTypeName": pt.PhoneTypeName
            } for pt in phonetypes
        ])
    except Exception as e:
        return jsonify({"error": str(e)}), 500



# =========================================GET ALL PHONETYPE ID=========================

@api_blueprint.route('/api/phonetypes/<int:phonetype_id>', methods=['GET'])
def get_phonetype(phonetype_id):
    try:
        phonetype = PhoneTypes.query.get(phonetype_id)
        if not phonetype:
            return jsonify({"error": "PhoneType not found"}), 404
        return jsonify({
            "PhoneTypeID": phonetype.PhoneTypeID,
            "PhoneTypeName": phonetype.PhoneTypeName
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# =====================================POST======================
@api_blueprint.route('/api/phonetypes', methods=['POST'])
def add_phonetype():
    data = request.get_json()
    if not all(key in data for key in ['PhoneTypeName']):
        return jsonify({"error": "Missing required field: PhoneTypeName"}), 400

    try:
        phonetype = PhoneTypes(PhoneTypeName=data['PhoneTypeName'])
        db.session.add(phonetype)
        db.session.commit()
        return jsonify({
            "PhoneTypeID": phonetype.PhoneTypeID,
            "message": "PhoneType created"
        }), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "PhoneTypeName must be unique"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# ===========================================PUT===================
@api_blueprint.route('/api/phonetypes/<int:phonetype_id>', methods=['PUT'])
def update_phonetype(phonetype_id):
    data = request.get_json()
    try:
        phonetype = PhoneTypes.query.get(phonetype_id)
        if not phonetype:
            return jsonify({"error": "PhoneType not found"}), 404

        if 'PhoneTypeName' in data:
            phonetype.PhoneTypeName = data['PhoneTypeName']

        db.session.commit()
        return jsonify({
            "PhoneTypeID": phonetype.PhoneTypeID,
            "message": "PhoneType updated"
        })
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "PhoneTypeName must be unique"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500




#===========================DELETE PHONETYPE ID=============
@api_blueprint.route('/api/phonetypes/<int:phonetype_id>', methods=['DELETE'])
def delete_phonetype(phonetype_id):
    try:
        phonetype = PhoneTypes.query.get(phonetype_id)
        if not phonetype:
            return jsonify({"error": "PhoneType not found"}), 404
        db.session.delete(phonetype)
        db.session.commit()
        return jsonify({"message": "PhoneType deleted"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500



# ---------------------------------------------USERS-----------------------------------
# ========================================GET ALL USERS======================
@api_blueprint.route('/api/users', methods=['GET'])
def get_users():
    try:
        users = Users.query.all()
        return jsonify([{
            "UserID": user.UserID,
            "FirstName": user.FirstName,
            "LastName": user.LastName,
            "Mobile": user.Mobile,
            "SectionID": user.SectionID,
            "SectionName": user.section.SectionName if user.section else None,
            "JobID": user.JobID,
            "JobTitle": user.job.JobTitle if user.job else None,
            "is_admin": user.is_admin,
            "IsActive": user.IsActive
        } for user in users])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#=======================================GET SINGLE USER =================
@api_blueprint.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = Users.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        return jsonify({
            "UserID": user.UserID,
            "FirstName": user.FirstName,
            "LastName": user.LastName,
            "Mobile": user.Mobile,
            "is_admin": user.is_admin,
            "IsActive": user.IsActive
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ========================================POST===================================
@api_blueprint.route('/api/users', methods=['POST'])
def add_user():
    data = request.get_json()
    required_fields = ['FirstName', 'LastName', 'SectionID', 'JobID', 'Mobile']
    if not all(key in data for key in required_fields):
        return jsonify({"error": f"Missing required fields: {', '.join(required_fields)}"}), 400

    try:
        # Check if SectionID and JobID exist
        section = Sections.query.get(data['SectionID'])
        job = Jobs.query.get(data['JobID'])
        if not section or not job:
            return jsonify({"error": "Invalid SectionID or JobID"}), 400

        user = Users(
            FirstName=data['FirstName'],
            LastName=data['LastName'],
            SectionID=data['SectionID'],
            JobID=data['JobID'],
            Mobile=data['Mobile'],
            is_admin=data.get('is_admin', False),
            IsActive=data.get('IsActive', True)
        )
        db.session.add(user)
        db.session.commit()
        return jsonify({
            "UserID": user.UserID,
            "message": "User created"
        }), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Mobile must be unique"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# =============================================PUT==============
@api_blueprint.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    try:
        user = Users.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        if 'FirstName' in data:
            user.FirstName = data['FirstName']
        if 'LastName' in data:
            user.LastName = data['LastName']
        if 'Mobile' in data:
            user.Mobile = data['Mobile']
        if 'is_admin' in data:
            user.is_admin = data['is_admin']
        if 'IsActive' in data:
            user.IsActive = data['IsActive']
        if 'SectionID' in data:
            section = Sections.query.get(data['SectionID'])
            if not section:
                return jsonify({"error": "Invalid SectionID"}), 400
            user.SectionID = data['SectionID']
        if 'JobID' in data:
            job = Jobs.query.get(data['JobID'])
            if not job:
                return jsonify({"error": "Invalid JobID"}), 400
            user.JobID = data['JobID']

        db.session.commit()
        return jsonify({
            "UserID": user.UserID,
            "message": "User updated"
        })
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Mobile must be unique"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ==============================DELETE USER ===================
@api_blueprint.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user = Users.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# -------------------------------jobs-------------------------
# ====================================GET ALL JOBS==================
# ---------------------------------- JOBS --------------------------------
@api_blueprint.route('/api/jobs', methods=['GET'])
def get_jobs():
    try:
        jobs = Jobs.query.all()
        return jsonify([{
            "JobID": job.JobID,
            "JobTitle": job.JobTitle,
            "SectionID": job.SectionID
        } for job in jobs])
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_blueprint.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    try:
        job = Jobs.query.get(job_id)
        if not job:
            return jsonify({"error": "Job not found"}), 404
        return jsonify({
            "JobID": job.JobID,
            "JobTitle": job.JobTitle,
            "SectionID": job.SectionID,
            "SectionName": job.section.SectionName if job.section else None
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
# ===============================POST =======================
@api_blueprint.route('/jobs', methods=['POST'])
def add_job():
    data = request.get_json()

    # Validate required fields
    if not data or 'JobTitle' not in data or 'SectionID' not in data:
        return jsonify({'error': 'Missing JobTitle or SectionID'}), 400

    job_title = data['JobTitle']
    section_id = data['SectionID']

    # Optional: Check if SectionID exists
    section = Sections.query.get(section_id)
    if not section:
        return jsonify({'error': 'SectionID does not exist'}), 400

    # Create new job
    new_job = Jobs(JobTitle=job_title, SectionID=section_id)

    try:
        db.session.add(new_job)
        db.session.commit()
        return jsonify({
            'message': 'Job added successfully',
            'JobID': new_job.JobID,
            'JobTitle': new_job.JobTitle,
            'SectionID': new_job.SectionID
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# Delete a job by ID
@api_blueprint.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    try:
        job = Jobs.query.get(job_id)
        if not job:
            return jsonify({"error": "Job not found"}), 404
        db.session.delete(job)
        db.session.commit()
        return jsonify({"message": "Job deleted"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Update a job by ID
@api_blueprint.route('/api/jobs/<int:job_id>', methods=['PUT'])
def update_job(job_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    try:
        job = Jobs.query.get(job_id)
        if not job:
            return jsonify({"error": "Job not found"}), 404
        if 'JobTitle' in data:
            job.JobTitle = data['JobTitle']
        if 'SectionID' in data:
            job.SectionID = data['SectionID']
        db.session.commit()
        return jsonify({
            "JobID": job.JobID,
            "JobTitle": job.JobTitle,
            "SectionID": job.SectionID,
            "SectionName": job.section.SectionName if job.section else None,
            "message": "Job updated"
        })
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Invalid SectionID or database constraint violation"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ==================================== LOGIN==============
@api_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    # Validate input
    if not all(key in data for key in ['UserID', 'password']):
        return jsonify({"error": "Missing required fields: UserID, password"}), 400

    try:
        # Query user from database
        user = Users.query.filter_by(UserID=data['UserID']).first()

        if not user:
            return jsonify({"error": "نام کاربری یا رمز عبور اشتباه است"}), 401

        # Check password (assuming plaintext for now)
        if str(user.password) != str(data['password']):
            return jsonify({"error": "نام کاربری یا رمز عبور اشتباه است"}), 401

        if not user.IsActive:
            return jsonify({"error": "نام کاربری غیرفعال است"}), 403

        # Successful login response
        return jsonify({
            "UserID": user.UserID,
            "FirstName": user.FirstName,
            "LastName": user.LastName,
            "Mobile": user.Mobile,
            "is_admin": int(user.is_admin),
            "message": "Login successful"
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==================================== SEARCH==============



from sqlalchemy import or_, func

@api_blueprint.route('/search', methods=['GET'])
def search():
    import re
    query = request.args.get('q', '').strip()

    if not query:
        return jsonify([])

    # Normalize query: convert tabs/multiple spaces to a single space
    query = re.sub(r'\s+', ' ', query)

    try:
        # Concatenated name expressions
        full_name_1 = func.concat(Users.FirstName, ' ', Users.LastName)
        full_name_2 = func.concat(Users.LastName, ' ', Users.FirstName)

        users = (
            Users.query
            .join(Sections, Users.SectionID == Sections.SectionID)
            .join(Jobs, Users.JobID == Jobs.JobID)
            .outerjoin(PhoneNumbers, Jobs.JobID == PhoneNumbers.JobID)
            .outerjoin(PhoneTypes, PhoneNumbers.PhoneTypeID == PhoneTypes.PhoneTypeID)
            .filter(
                or_(
                    Users.FirstName.ilike(f'%{query}%'),
                    Users.LastName.ilike(f'%{query}%'),
                    full_name_1.ilike(f'%{query}%'),
                    full_name_2.ilike(f'%{query}%'),
                    Sections.SectionName.ilike(f'%{query}%'),
                    Jobs.JobTitle.ilike(f'%{query}%'),
                    PhoneNumbers.PhoneNumber.ilike(f'%{query}%'),
                    Users.Mobile.ilike(f'%{query}%')
                )
            )
            .all()
        )

        result = []
        for user in users:
            phone_numbers = [
                {
                    "PhoneNumber": pn.PhoneNumber,
                    "PhoneTypeName": pn.phone_type.PhoneTypeName if pn.phone_type else None
                }
                for pn in user.job.phone_numbers
            ]

            result.append({
                "UserID": user.UserID,
                "FirstName": user.FirstName,
                "LastName": user.LastName,
                "SectionName": user.section.SectionName,
                "JobTitle": user.job.JobTitle,
                "Mobile": user.Mobile,
                "PhoneNumbers": phone_numbers
            })

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500



