from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db import connection
from datetime import datetime, time
from django.utils import timezone



def show(request):
    return render(request,'index.html')

def student_register(request):
    if request.method == 'POST':
        stud_id = request.POST.get('stud_id')
        name = request.POST.get('name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        course_name = request.POST.get('course_name')
        image = request.FILES.get('image')
        username = request.POST.get('username')
        password = request.POST.get('password')


        if not stud_id:
            return HttpResponse(
                "<script>alert('Student ID is required');window.location='/register';</script>"
            )

        if not phone.isdigit():
            return HttpResponse(
                "<script>alert('Phone number must contain only digits');window.location='/register';</script>"
            )

        if len(phone) != 10:
            return HttpResponse(
                "<script>alert('Phone number must be exactly 10 digits');window.location='/register';</script>"
            )

        cursor = connection.cursor()
        cursor.execute(
            "SELECT stud_id FROM student_register WHERE stud_id=%s",
            [stud_id]
        )

        if cursor.fetchone():
            return HttpResponse(
                "<script>alert('Student ID already exists!');window.location='/register';</script>"
            )

        cursor.execute("""
            INSERT INTO student_register
            (name, address, phone, stud_id, course_name, image,username, password)
            VALUES (%s, %s, %s, %s, %s, %s, %s,%s)
        """, [name, address, phone, stud_id, course_name, image,username, password])

        return HttpResponse(
            "<script>alert('Registration Successful');window.location='/login';</script>"
        )

        return redirect(login)

    return render(request, 'students_registration.html')



def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        print("username:", username)
        print("password:", password)
        print(request.POST)


        if username == 'admin' and password == 'admin':
            request.session['admin'] = True
            return redirect(admin_home)

        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM student_register WHERE username=%s AND password=%s",
            [username, password]
        )
        student = cursor.fetchone()

        if student:
            request.session['stud_id'] = student[0]
            return redirect(student_home)


        cursor.execute(
            "SELECT * FROM staff_register WHERE username=%s AND password=%s",
            [username, password]
        )
        staff = cursor.fetchone()

        if staff:
            request.session['staff_id'] = staff[0]
            request.session['staff_type'] = staff[2] # staff_type
            return redirect(staff_home)

        return render(request, 'login.html', {
            'error': 'Invalid username or password'
        })

    return render(request, 'login.html')

def admin_home(request):
    if not request.session.get('admin'):
        return redirect(login)
    return render(request, 'admin_home.html')


def student_home(request):
    if not request.session.get('stud_id'):
        return redirect(login)
    return render(request, 'student_home.html')

def staff_home(request):
    if not request.session.get('staff_id'):
        return redirect(login)
    return render(request, 'staff_home.html')

def logout(request):
    request.session.flush()
    return redirect(show)



def staff_register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        staff_type = request.POST.get('staff_type')
        designation = request.POST.get('designation')
        experience = request.POST.get('experience')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        staff_image = request.FILES.get('staff_image')


        #
        # if not staff_id:
        #     return HttpResponse(
        #         "<script>alert('Student ID is required');window.location='/register';</script>"
        #     )
        #
        # if not phone.isdigit():
        #     return HttpResponse(
        #         "<script>alert('Phone number must contain only digits');window.location='/register';</script>"
        #     )
        #
        # if len(phone) != 10:
        #     return HttpResponse(
        #         "<script>alert('Phone number must be exactly 10 digits');window.location='/register';</script>"
        #     )

        cursor = connection.cursor()


        cursor.execute(
            "SELECT staff_id FROM staff_register WHERE username=%s",
            [username]
        )
        if cursor.fetchone():
            return HttpResponse(
                "<script>alert('Username already exists');window.history.back();</script>"
            )


        cursor.execute("""
            INSERT INTO staff_register
            (name, staff_type, designation, experience,
             phone, email, staff_image, username, password)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, [
            name, staff_type, designation, experience,
            phone, email, staff_image, username, password
        ])

        return HttpResponse(
            "<script>alert('Staff Registered Successfully');window.location='/login';</script>"
        )

    return render(request, 'staff_registration.html')

def admin_view_students(request):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM student_register")
    rows = cursor.fetchall()

    students = []
    for row in rows:
        students.append({
            'stud_id': row[0],
            'name': row[1],
            'address': row[2],
            'phone': row[3],
            'course_name': row[4],
            'image': row[5],
        })

    return render(request, 'admin_view_student.html', {'students': students})

def admin_view_staff(request):
    if not request.session.get('admin'):
        return redirect('login')

    cursor = connection.cursor()
    cursor.execute("""
        SELECT staff_id,name, staff_type,phone,email,username,status,experience,designation,staff_image FROM staff_register
    """)
    staff_list = cursor.fetchall()

    return render(request, 'admin_view_staff.html', {
        'staff_list': staff_list
    })

def view_profile(request):
    stud_id = request.session.get('stud_id')
    if not stud_id:
        return redirect(login)

    cursor = connection.cursor()
    cursor.execute(
        "SELECT stud_id, name, address, phone, course_name, image FROM student_register WHERE stud_id=%s",
        [stud_id]
    )
    row = cursor.fetchone()

    student = {
        'stud_id': row[0],
        'name': row[1],
        'address': row[2],
        'phone': row[3],
        'course_name': row[4],
        'image': row[5],
    }

    return render(request, 'view_profile.html', {'student': student})


def edit_profile(request, stud_id):
    cursor = connection.cursor()


    cursor.execute(
        "SELECT stud_id, name, address, phone, course_name, image FROM student_register WHERE stud_id=%s",
        [stud_id]
    )
    row = cursor.fetchone()

    if not row:
        return redirect('view_profile')

    student = {
        'stud_id': row[0],
        'name': row[1],
        'address': row[2],
        'phone': row[3],
        'course_name': row[4],
        'image': row[5],
    }

    if request.method == "POST":
        name = request.POST.get('name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        course_name = request.POST.get('course_name')

        image = request.FILES.get('image')


        if image:
            cursor.execute("""
                UPDATE student_register
                SET name=%s, address=%s, phone=%s, course_name=%s, image=%s
                WHERE stud_id=%s
            """, [name, address, phone, course_name, image, stud_id])
        else:
            cursor.execute("""
                UPDATE student_register
                SET name=%s, address=%s, phone=%s, course_name=%s
                WHERE stud_id=%s
            """, [name, address, phone, course_name, stud_id])

        return redirect('view_profile')

    return render(request, "edit_profile.html", {"student": student})


def search_form(request):
    return render(request, 'search_student.html')


def search_result(request):
    students = []
    query = request.GET.get('q')

    if query:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT stud_id, name, phone, course_name
            FROM student_register
            WHERE name LIKE %s
               OR stud_id LIKE %s
               OR phone LIKE %s
        """, [
            f"%{query}%",
            f"%{query}%",
            f"%{query}%"
        ])
        students = cursor.fetchall()

    return render(request, 'search_result.html', {'students': students})


def send_request(request):
    if request.method == "POST":
        roll_no = request.POST.get('roll_no')
        reason = request.POST.get('reason')
        out_time_str = request.POST.get('out_time')
        in_time_str = request.POST.get('in_time')
        request_date = datetime.now()

        try:
            out_parts = out_time_str.split(':')
            in_parts = in_time_str.split(':')
            
            out_time = datetime(
                year=request_date.year,
                month=request_date.month,
                day=request_date.day,
                hour=int(out_parts[0]),
                minute=int(out_parts[1])
            )
            
            in_time = datetime(
                year=request_date.year,
                month=request_date.month,
                day=request_date.day,
                hour=int(in_parts[0]),
                minute=int(in_parts[1])
            )
        except (ValueError, IndexError) as e:
            return HttpResponse(
                f"<script>alert('Invalid time format. Please use HH:MM format.');window.location='/send_request';</script>"
            )

        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO gate_pass_details 
            (roll_no, reason, out_time, in_time, request_date)
            VALUES (%s, %s, %s, %s, %s)
        """, [roll_no, reason, out_time, in_time, request_date])

        return redirect(student_view_requests)

    return render(request, 'send_gatepass_request.html')


def view_requests(request):

    if not request.session.get('admin'):
        return redirect(login)

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT request_detail_id, roll_no, reason, out_time, in_time, request_date, status
            FROM gate_pass_details
            ORDER BY request_date DESC
        """)
        rows = cursor.fetchall()

    requests = []
    for row in rows:
        requests.append({
            'request_detail_id': row[0],
            'roll_no': row[1],
            'reason': row[2],
            'out_time': row[3],
            'in_time': row[4],
            'request_date': row[5],
            'status': row[6]
        })

    return render(request, 'admin_view_gate_pass_request.html', {'requests': requests})


def student_view_requests(request):
    stud_id = request.session.get('stud_id')
    if not stud_id:
        return redirect(login)

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT request_detail_id, roll_no, reason, out_time, in_time, request_date, status
            FROM gate_pass_details
            WHERE roll_no = %s
            ORDER BY request_date DESC
        """, [stud_id])
        rows = cursor.fetchall()

    requests = []
    for row in rows:
        requests.append({
            'request_detail_id': row[0],
            'roll_no': row[1],
            'reason': row[2],
            'out_time': row[3],
            'in_time': row[4],
            'request_date': row[5],
            'status': row[6]
        })

    return render(request, 'student_view_gate_pass_request.html', {'requests': requests})


def staff_view_requests(request):
    if not request.session.get('staff_id'):
        return redirect(login)

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT request_detail_id, roll_no, reason, out_time, in_time, request_date, status
            FROM gate_pass_details
            ORDER BY request_date DESC
        """)
        rows = cursor.fetchall()

    requests = []
    for row in rows:
        requests.append({
            'request_detail_id': row[0],
            'roll_no': row[1],
            'reason': row[2],
            'out_time': row[3],
            'in_time': row[4],
            'request_date': row[5],
            'status': row[6]
        })

    return render(request, 'staff_view_gate_pass_request.html', {'requests': requests})


def approve_request(request, request_id):
    if not request.session.get('admin'):
        return redirect(login)

    cursor = connection.cursor()
    cursor.execute("""
        UPDATE gate_pass_details
        SET status = 'Approved'
        WHERE request_detail_id = %s
    """, [request_id])

    return redirect('view_requests')


def reject_request(request, request_id):
    if not request.session.get('admin'):
        return redirect(login)

    cursor = connection.cursor()
    cursor.execute("""
        UPDATE gate_pass_details
        SET status = 'Rejected'
        WHERE request_detail_id = %s
    """, [request_id])

    return redirect(view_requests)

def view_approved_gate_pass(request):
    stud_id = request.session.get('stud_id')

    if not stud_id:
        return redirect(login)

    cursor = connection.cursor()
    cursor.execute("""
        SELECT request_detail_id, reason, out_time, in_time, request_date
        FROM gate_pass_details
        WHERE (roll_no = %s OR stud_id = %s) AND status = 'Approved'
        ORDER BY request_date DESC
    """, [stud_id, stud_id])

    rows = cursor.fetchall()
    data = []
    for row in rows:
        data.append({
            'request_detail_id': row[0],
            'reason': row[1],
            'out_time': row[2],
            'in_time': row[3],
            'request_date': row[4]
        })

    return render(request, 'view_approved_gate_pass.html', {'data': data})

# def track_student_movement(request):
#     if not request.session.get('admin') and not request.session.get('staff_id'):
#         return redirect(login)
#
#     cursor = connection.cursor()
#     # Include records with 'Approved' status OR empty status (treat as approved)
#     cursor.execute("""
#         SELECT
#             g.request_detail_id,
#             s.stud_id,
#             s.name,
#             g.reason,
#             g.out_time,
#             g.in_time,
#             s.image
#         FROM gate_pass_details g
#         JOIN student_register s
#             ON (g.roll_no = s.stud_id OR g.stud_id = s.stud_id)
#         WHERE g.status = 'Approved' OR g.status = ''
#         ORDER BY g.request_detail_id DESC
#     """)
#
#     rows = cursor.fetchall()
#     data = []
#     for row in rows:
#         print(f"\nDEBUG Processing request_id: {row[0]}, student: {row[2]}")
#         out_val = row[4]
#         in_val = row[5]
#         print(f"  Raw values - out_time: {out_val} (type: {type(out_val).__name__}), in_time: {in_val} (type: {type(in_val).__name__})")
#
#         # Determine status based on whether staff has marked actual departure/arrival
#         # Student provides expected times (HH:MM format)
#         # Staff marks with actual datetime (YYYY-MM-DD HH:MM:SS format)
#         status = 'PENDING'
#
#         def is_actually_marked(val):
#             # Check if value indicates staff has physically marked attendance
#             if val is None:
#                 return False
#             # If it's a datetime object, it was marked by staff (full timestamp)
#             if isinstance(val, datetime):
#                 print(f"DEBUG: Value {val} is datetime instance")
#                 return True
#             # If it's a time object, it's just the expected time from student
#             if isinstance(val, time):
#                 print(f"DEBUG: Value {val} is time object (student's expected time)")
#                 return False
#             # Convert to string and check format
#             str_val = str(val).strip()
#             print(f"DEBUG: Checking value '{str_val}' (length: {len(str_val)})")
#             # Time format from student: "HH:MM:SS" (8 chars)
#             # Datetime from staff marking: "YYYY-MM-DD HH:MM:SS..." (19+ chars)
#             if len(str_val) >= 16:
#                 print(f"DEBUG: Value identified as marked (datetime format)")
#                 return True
#             print(f"DEBUG: Value identified as expected time (time format only)")
#             return False
#
#         if is_actually_marked(in_val):
#             status = 'IN'
#         elif is_actually_marked(out_val):
#             status = 'OUT'
#
#         image_name = row[6] if row[6] else ""
#         if image_name and not str(image_name).startswith('http'):
#             image_url = f"/media/{image_name}"
#         else:
#             image_url = image_name or "/static/img/default-user.png"
#
#         data.append({
#             'request_detail_id': row[0],
#             'stud_id': row[1],
#             'name': row[2],
#             'reason': row[3],
#             'movement_status': status,
#             'image': image_url
#         })
#
#     return render(request, "track_student_movement.html", {"data": data})
#
#
# def mark_student_out(request, request_id):
#     if not request.session.get('admin') and not request.session.get('staff_id'):
#         return redirect(login)
#
#     current_time = timezone.now()
#     print(f"\n{'='*60}")
#     print(f"Marking OUT - Request ID: {request_id}, Time: {current_time}")
#     print(f"Session admin: {request.session.get('admin')}, staff_id: {request.session.get('staff_id')}")
#
#     with connection.cursor() as cursor:
#         # First check if the record exists and what its status is
#         cursor.execute("""
#             SELECT request_detail_id, status, out_time, in_time
#             FROM gate_pass_details
#             WHERE request_detail_id = %s
#         """, [request_id])
#         before_update = cursor.fetchone()
#         if before_update:
#             print(f"Before update - ID: {before_update[0]}, Status: {before_update[1]}, Out: {before_update[2]}, In: {before_update[3]}")
#         else:
#             print(f"ERROR: Record with ID {request_id} not found!")
#
#         # Now try to update
#         cursor.execute("""
#             UPDATE gate_pass_details
#             SET out_time = %s
#             WHERE request_detail_id = %s
#               AND (status = 'Approved' OR status = '')
#         """, [current_time, request_id])
#
#         print(f"Rows updated: {cursor.rowcount}")
#
#         if cursor.rowcount == 0:
#             print(f"WARNING: No rows updated! Either record doesn't exist or status is not 'Approved'")
#             # Try updating without status check to see if that's the issue
#             cursor.execute("""
#                 UPDATE gate_pass_details
#                 SET out_time = %s
#                 WHERE request_detail_id = %s
#             """, [current_time, request_id])
#             print(f"Rows updated (without status check): {cursor.rowcount}")
#
#         # Verify the update
#         cursor.execute("""
#             SELECT request_detail_id, out_time, in_time FROM gate_pass_details WHERE request_detail_id = %s
#         """, [request_id])
#         result = cursor.fetchone()
#         if result:
#             print(f"After update - ID: {result[0]}, out_time: {result[1]}, in_time: {result[2]}")
#
#         print(f"{'='*60}\n")
#
#     return redirect(track_student_movement)
#
# def mark_student_in(request, request_id):
#     if not request.session.get('admin') and not request.session.get('staff_id'):
#         return redirect(login)
#
#     current_time = timezone.now()
#     print(f"\n{'='*60}")
#     print(f"Marking IN - Request ID: {request_id}, Time: {current_time}")
#
#     with connection.cursor() as cursor:
#         # Check before update
#         cursor.execute("""
#             SELECT request_detail_id, status, out_time, in_time
#             FROM gate_pass_details
#             WHERE request_detail_id = %s
#         """, [request_id])
#         before_update = cursor.fetchone()
#         if before_update:
#             print(f"Before update - ID: {before_update[0]}, Status: {before_update[1]}, Out: {before_update[2]}, In: {before_update[3]}")
#         else:
#             print(f"ERROR: Record with ID {request_id} not found!")
#
#         # Update
#         cursor.execute("""
#             UPDATE gate_pass_details
#             SET in_time = %s
#             WHERE request_detail_id = %s
#               AND status = 'Approved'
#         """, [current_time, request_id])
#
#         print(f"Rows updated: {cursor.rowcount}")
#
#         if cursor.rowcount == 0:
#             print(f"WARNING: No rows updated! Either record doesn't exist or status is not 'Approved'")
#             cursor.execute("""
#                 UPDATE gate_pass_details
#                 SET in_time = %s
#                 WHERE request_detail_id = %s
#             """, [current_time, request_id])
#             print(f"Rows updated (without status check): {cursor.rowcount}")
#
#         # Verify
#         cursor.execute("""
#             SELECT request_detail_id, out_time, in_time FROM gate_pass_details WHERE request_detail_id = %s
#         """, [request_id])
#         result = cursor.fetchone()
#         if result:
#             print(f"After update - ID: {result[0]}, out_time: {result[1]}, in_time: {result[2]}")
#
#         print(f"{'='*60}\n")
#
#     return redirect(track_student_movement)


from django.shortcuts import render, redirect
from django.db import connection
from django.utils import timezone


def track_student_movement(request):

    if not request.session.get('admin') and not request.session.get('staff_id'):
        return redirect('login')

    cursor = connection.cursor()

    cursor.execute("""
        SELECT 
            g.request_detail_id,
            s.stud_id,
            s.name,
            g.reason,
            g.out_time,
            g.in_time,
            s.image
        FROM gate_pass_details g
        JOIN student_register s 
        ON (g.roll_no = s.stud_id OR g.stud_id = s.stud_id)
        WHERE g.status = 'Approved'
        ORDER BY g.request_detail_id DESC
    """)

    rows = cursor.fetchall()

    data = []

    for row in rows:

        request_detail_id = row[0]
        stud_id = row[1]
        name = row[2]
        reason = row[3]
        out_time = row[4]
        in_time = row[5]
        image = row[6]

        if in_time:
            status = "IN"
        elif out_time:
            status = "OUT"
        else:
            status = "PENDING"

        if image:
            if isinstance(image, bytes):
                image_name = image.decode('utf-8')
            else:
                image_name = str(image)
            image_url = f"/media/{image_name}"
        else:
            image_url = "/static/img/default-user.png"

        data.append({
            "request_detail_id": request_detail_id,
            "stud_id": stud_id,
            "name": name,
            "reason": reason,
            "movement_status": status,
            "image": image_url
        })

    return render(request, "track_student_movement.html", {"data": data})



def mark_student_out(request, request_id):

    if not request.session.get('admin') and not request.session.get('staff_id'):
        return redirect('login')

    cursor = connection.cursor()

    cursor.execute("""
        UPDATE gate_pass_details
        SET out_time = %s
        WHERE request_detail_id = %s
        AND status = 'Approved'
    """, [timezone.now(), request_id])


    cursor.execute("SELECT stud_id FROM gate_pass_details WHERE request_detail_id = %s", [request_id])
    row = cursor.fetchone()
    if row:
        cursor.execute("""
            INSERT INTO gate_pass_history (stud_id, passing_date)
            VALUES (%s, NOW())
        """, [row[0]])

    return redirect('track_student_movement')



def mark_student_in(request, request_id):

    if not request.session.get('admin') and not request.session.get('staff_id'):
        return redirect('login')

    cursor = connection.cursor()

    cursor.execute("""
        UPDATE gate_pass_details
        SET in_time = %s
        WHERE request_detail_id = %s
        AND status = 'Approved'
    """, [timezone.now(), request_id])

    cursor.execute("SELECT stud_id FROM gate_pass_details WHERE request_detail_id = %s", [request_id])
    row = cursor.fetchone()
    if row:
        cursor.execute("""
            INSERT INTO gate_pass_history (stud_id, passing_date)
            VALUES (%s, NOW())
        """, [row[0]])

    return redirect('track_student_movement')


def nfc_scan(request):

    if request.method == 'POST':
        tag_uid = request.POST.get('tag_uid') or request.POST.get('stud_id') or request.POST.get('roll_no')

        if not tag_uid:
            return HttpResponse(
                "<script>alert('No NFC tag ID received');window.history.back();</script>"
            )

        print(f"\n{'='*60}")
        print(f"NFC Scan - Tag UID: {tag_uid}")

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT stud_id FROM nfc_tags WHERE tag_uid = %s LIMIT 1
            """, [tag_uid])
            tag_row = cursor.fetchone()

            if tag_row:
                stud_id = tag_row[0]
                print(f"Tag UID {tag_uid} resolved to student ID: {stud_id}")
            else:
                stud_id = tag_uid
                print(f"Tag UID not in nfc_tags, treating as student ID: {stud_id}")

            cursor.execute("""
                SELECT request_detail_id, out_time, in_time, reason
                FROM gate_pass_details
                WHERE (roll_no = %s OR stud_id = %s)
                  AND (status = 'Approved' OR status = '')
                ORDER BY request_date DESC
                LIMIT 1
            """, [stud_id, stud_id])

            gate_pass = cursor.fetchone()

            if not gate_pass:
                print(f"No approved gate pass found for student {stud_id}")
                return HttpResponse(
                    f"<script>alert('No approved gate pass found for student {stud_id}');window.location='/track_student_movement';</script>"
                )

            request_id, current_out, current_in, reason = gate_pass
            print(f"Found gate pass ID: {request_id}, Out: {current_out}, In: {current_in}")

            is_out_marked = current_out is not None and isinstance(current_out, datetime)
            is_in_marked  = current_in  is not None and isinstance(current_in,  datetime)

            current_time = timezone.now()

            if not is_out_marked:
                cursor.execute("""
                    UPDATE gate_pass_details
                    SET out_time = %s
                    WHERE request_detail_id = %s
                """, [current_time, request_id])

                cursor.execute(
                    "SELECT name FROM student_register WHERE stud_id = %s", [stud_id]
                )
                student_row = cursor.fetchone()
                student_name = student_row[0] if student_row else "Student"

                message = f"✓ {student_name} marked OUT at {current_time.strftime('%H:%M:%S')}"
                print(f"Action: MARKED OUT - {message}")

                cursor.execute("""
                    INSERT INTO gate_pass_history (stud_id, passing_date)
                    VALUES (%s, NOW())
                """, [stud_id])

            elif is_out_marked and not is_in_marked:
                cursor.execute("""
                    UPDATE gate_pass_details
                    SET in_time = %s
                    WHERE request_detail_id = %s
                """, [current_time, request_id])

                cursor.execute(
                    "SELECT name FROM student_register WHERE stud_id = %s", [stud_id]
                )
                student_row = cursor.fetchone()
                student_name = student_row[0] if student_row else "Student"

                message = f"✓ {student_name} marked IN at {current_time.strftime('%H:%M:%S')}"
                print(f"Action: MARKED IN - {message}")

                cursor.execute("""
                    INSERT INTO gate_pass_history (stud_id, passing_date)
                    VALUES (%s, NOW())
                """, [stud_id])

            else:
                message = "Student has already completed their movement (both IN and OUT marked)"
                print(f"Warning: {message}")

        print(f"{'='*60}\n")

        return HttpResponse(
            f"<script>alert('{message}');window.location='/track_student_movement';</script>"
        )

    return HttpResponse("<script>alert('Invalid request method');window.history.back();</script>")



# def assign_nfc_tag(request):
#     """Admin view to assign an NFC tag UID to a student."""
#     if not request.session.get('admin'):
#         return redirect('login')
# 
#     message = None
#     existing_tag = None
#     students = []
# 
#     with connection.cursor() as cursor:
#         cursor.execute("SELECT stud_id, name FROM student_register ORDER BY name")
#         students = cursor.fetchall()
#         cursor.execute("SELECT staff_id, name, staff_type FROM staff_register ORDER BY name")
#         staffs = cursor.fetchall()
#         cursor.execute("SELECT staff_id, name, staff_type FROM staff_register ORDER BY name")
#         staffs = cursor.fetchall()
# 
#     if request.method == 'POST':
#         stud_id = request.POST.get('stud_id', '').strip()
#         tag_uid  = request.POST.get('tag_uid',  '').strip()
# 
#         if not stud_id or not tag_uid:
#             message = ('error', 'Both Student ID and NFC Tag UID are required.')
#         else:
#             with connection.cursor() as cursor:
#                 cursor.execute(
#                     "SELECT stud_id FROM nfc_tags WHERE tag_uid = %s", [tag_uid]
#                 )
#                 conflict = cursor.fetchone()
# 
#                 if conflict and conflict[0] != stud_id:
#                     message = ('error', f'Tag UID "{tag_uid}" is already assigned to student {conflict[0]}. Remove it first.')
#                 else:
#                     cursor.execute(
#                         "SELECT id FROM nfc_tags WHERE stud_id = %s", [stud_id]
#                     )
#                     existing = cursor.fetchone()
# 
#                     if existing:
#                         cursor.execute(
#                             "UPDATE nfc_tags SET tag_uid = %s, assigned_at = NOW() WHERE stud_id = %s",
#                             [tag_uid, stud_id]
#                         )
#                         message = ('success', f'NFC tag updated successfully for student {stud_id}.')
#                     else:
#                         cursor.execute(
#                             "INSERT INTO nfc_tags (tag_uid, stud_id, assigned_at) VALUES (%s, %s, NOW())",
#                             [tag_uid, stud_id]
#                         )
#                         message = ('success', f'NFC tag assigned successfully to student {stud_id}.')
# 
#     selected_stud_id = request.GET.get('stud_id') or request.POST.get('stud_id')
#     if selected_stud_id:
#         with connection.cursor() as cursor:
#             cursor.execute(
#                 "SELECT tag_uid FROM nfc_tags WHERE stud_id = %s", [selected_stud_id]
#             )
#             row = cursor.fetchone()
#             existing_tag = row[0] if row else None
# 
#     return render(request, 'assign_nfc_tag.html', {
#         'staffs': staffs,
#         'students':    students,
#         'message':     message,
#         'existing_tag': existing_tag,
#         'selected_stud_id': selected_stud_id,
#     })
# 
# 
def view_nfc_tags(request):
    """Admin view to see all NFC tag assignments."""
    if not request.session.get('admin'):
        return redirect('login')

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT n.id, n.tag_uid, n.stud_id, s.name, n.assigned_at
            FROM nfc_tags n
            JOIN student_register s ON n.stud_id = s.stud_id
            ORDER BY n.assigned_at DESC
        """)
        rows = cursor.fetchall()

    tags = []
    for row in rows:
        tags.append({
            'id':          row[0],
            'tag_uid':     row[1],
            'stud_id':     row[2],
            'name':        row[3],
            'assigned_at': row[4],
        })

    return render(request, 'view_nfc_tags.html', {'tags': tags})


def remove_nfc_tag(request, tag_id):
    """Admin view to remove an NFC tag assignment."""
    if not request.session.get('admin'):
        return redirect('login')

    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM nfc_tags WHERE id = %s", [tag_id])

    return redirect('view_nfc_tags')



from django.http import JsonResponse
from django.utils import timezone

def out_students_status(request):

    if not request.session.get('admin') and not request.session.get('staff_id'):
        return JsonResponse({'error': 'Unauthorised'}, status=403)

    today = timezone.localtime(timezone.now()).date()

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT h.stud_id, s.name, COUNT(*) as scan_count
            FROM gate_pass_history h
            JOIN student_register s ON h.stud_id = s.stud_id
            WHERE DATE(h.passing_date) = %s
            GROUP BY h.stud_id, s.name
        """, [today])
        rows = cursor.fetchall()

    students_out = []
    for row in rows:
        stud_id = row[0]
        name = row[1]
        count = row[2]
        if count % 2 == 0:
            students_out.append({'name': name, 'stud_id': stud_id})

    return JsonResponse({'count': len(students_out), 'students': students_out})


import pytz
from django.shortcuts import render
from django.db import connection


def view_gate_pass_history(request):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT 
            g.gate_pass_history_id,
            s.name,
            g.stud_id,
            g.passing_date,
            g.passing_time,
            g.auth_status
        FROM gate_pass_history g
        JOIN student_register s ON g.stud_id = s.stud_id
        ORDER BY g.stud_id ASC, g.gate_pass_history_id ASC
    """)

    rows = cursor.fetchall()

    india = pytz.timezone('Asia/Kolkata')
    london = pytz.timezone('Europe/London')

    student_scan_count = {}

    data = []

    for row in rows:
        gate_id  = row[0]
        name     = row[1]
        stud_id  = row[2]
        date_val = row[3]
        time_val = row[4]


        try:
            from datetime import date as date_type, time as time_type, timedelta


            if isinstance(date_val, datetime):
                d = date_val.date()
            elif isinstance(date_val, date_type):
                d = date_val
            else:
                d = datetime.strptime(str(date_val).strip(), "%Y-%m-%d").date()


            if isinstance(time_val, timedelta):
                total_seconds = int(time_val.total_seconds())
                h, rem = divmod(abs(total_seconds), 3600)
                m, s   = divmod(rem, 60)
                t = time_type(h % 24, m, s)
            elif isinstance(time_val, time_type):
                t = time_val
            elif isinstance(time_val, datetime):
                t = time_val.time()
            else:
                ts = str(time_val).strip()
                for fmt in ("%H:%M:%S", "%H:%M", "%I:%M %p", "%I:%M:%S %p"):
                    try:
                        t = datetime.strptime(ts, fmt).time()
                        break
                    except ValueError:
                        continue
                else:
                    raise ValueError(f"Unrecognised time format: {ts!r}")


            naive_dt  = datetime.combine(d, t)
            london_dt = london.localize(naive_dt)
            ist_dt    = london_dt.astimezone(india)
            formatted_time = ist_dt.strftime("%d-%m-%Y %I:%M %p")

        except Exception as e:
            print(f"[view_gate_pass_history] time conversion error: {e}")
            formatted_time = str(time_val) if time_val else "Invalid Time"


        student_scan_count[stud_id] = student_scan_count.get(stud_id, 0) + 1
        count = student_scan_count[stud_id]
        entry_type = "OUT" if count % 2 == 1 else "IN"

        data.append({
            'id':         gate_id,
            'name':       name,
            'time':       formatted_time,
            'entry_type': entry_type,
        })

    data.sort(key=lambda x: x['id'], reverse=True)

    return render(request, 'view_gate_pass.html', {'data': data})
def admin_view_gate_pass_history(request):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT 
            g.gate_pass_history_id,
            s.name,
            g.stud_id,
            g.passing_date,
            g.passing_time,
            g.auth_status
        FROM gate_pass_history g
        JOIN student_register s ON g.stud_id = s.stud_id
        ORDER BY g.stud_id ASC, g.gate_pass_history_id ASC
    """)

    rows = cursor.fetchall()

    india = pytz.timezone('Asia/Kolkata')
    london = pytz.timezone('Europe/London')

    student_scan_count = {}

    data = []

    for row in rows:
        gate_id  = row[0]
        name     = row[1]
        stud_id  = row[2]
        date_val = row[3]
        time_val = row[4]
        auth_status = row[5] if len(row) > 5 else 'Unknown'


        try:
            from datetime import date as date_type, time as time_type, timedelta

            if isinstance(date_val, datetime):
                d = date_val.date()
            elif isinstance(date_val, date_type):
                d = date_val
            else:
                d = datetime.strptime(str(date_val).strip(), "%Y-%m-%d").date()

            if isinstance(time_val, timedelta):
                total_seconds = int(time_val.total_seconds())
                h, rem = divmod(abs(total_seconds), 3600)
                m, s   = divmod(rem, 60)
                t = time_type(h % 24, m, s)
            elif isinstance(time_val, time_type):
                t = time_val
            elif isinstance(time_val, datetime):
                t = time_val.time()
            else:
                ts = str(time_val).strip()
                for fmt in ("%H:%M:%S", "%H:%M", "%I:%M %p", "%I:%M:%S %p"):
                    try:
                        t = datetime.strptime(ts, fmt).time()
                        break
                    except ValueError:
                        continue
                else:
                    raise ValueError(f"Unrecognised time format: {ts!r}")

            naive_dt  = datetime.combine(d, t)
            london_dt = london.localize(naive_dt)
            ist_dt    = london_dt.astimezone(india)
            formatted_time = ist_dt.strftime("%d-%m-%Y %I:%M %p")

        except Exception as e:
            print(f"[admin_view_gate_pass_history] time conversion error: {e}")
            formatted_time = str(time_val) if time_val else "Invalid Time"

        student_scan_count[stud_id] = student_scan_count.get(stud_id, 0) + 1
        count = student_scan_count[stud_id]
        entry_type = "OUT" if count % 2 == 1 else "IN"

        data.append({
            'id':         gate_id,
            'name':       name,
            'time':       formatted_time,
            'entry_type': entry_type,
            'auth_status': auth_status,
        })

    data.sort(key=lambda x: x['id'], reverse=True)

    return render(request, 'admin_view_gate_pass.html', {'data': data})

from django.contrib import messages

def mark_entry_exit(request, stud_id):
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO gate_pass_history (stud_id, passing_date)
        VALUES (%s, NOW())
    """, [stud_id])

    cursor.execute("SELECT name FROM student_register WHERE stud_id=%s", [stud_id])
    name = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM gate_pass_history WHERE stud_id=%s", [stud_id])
    count = cursor.fetchone()[0]

    status = "IN" if count % 2 == 1 else "OUT"

    messages.success(request, f"{name} marked as {status}")

    return redirect('gate_pass_history')

def get_latest_movement(request):
    if not request.session.get('admin'):
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT g.gate_pass_history_id, s.name, g.stud_id
            FROM gate_pass_history g
            JOIN student_register s ON g.stud_id = s.stud_id
            ORDER BY g.gate_pass_history_id DESC
            LIMIT 1
        """)
        row = cursor.fetchone()
        
        if row:
            history_id, name, stud_id = row
            
            # Count scans only for today for this student, to be more accurate about current pass
            today = timezone.localtime(timezone.now()).date()
            cursor.execute("""
                SELECT COUNT(*) FROM gate_pass_history 
                WHERE stud_id = %s AND DATE(passing_date) = %s
            """, [stud_id, today])
            count = cursor.fetchone()[0]
            
            # First scan today for an approved pass = OUT, Second = IN
            # count % 2 == 1 means 1st, 3rd... scans = OUT
            status = "OUT" if count % 2 == 1 else "IN"
            
            return JsonResponse({
                'id': history_id,
                'name': name,
                'status': status
            })
    
    return JsonResponse({'id': None})

def api_nfc_scan(request):
    if request.method == 'GET':
        tag_uid = request.GET.get('id')
        if not tag_uid:
            return JsonResponse({'status': '0', 'message': 'No tag ID received'})
        
        # Trim whitespace explicitly
        tag_uid = tag_uid.strip()

        with connection.cursor() as cursor:
            # Query standard and spacing-removed tag strings natively
            cursor.execute("SELECT stud_id FROM nfc_tags WHERE tag_uid = %s OR REPLACE(tag_uid, ' ', '') = %s LIMIT 1", [tag_uid, tag_uid])
            tag_row = cursor.fetchone()
            
            if not tag_row:
                # Capture the new unknown card to the database using random negative IDs to bypass UNIQUE constraints
                import random
                rand_id = -random.randint(100, 999999)
                cursor.execute("DELETE FROM nfc_tags WHERE tag_uid = %s", [tag_uid])
                cursor.execute("INSERT INTO nfc_tags (tag_uid, stud_id, assigned_at) VALUES (%s, %s, NOW())", [tag_uid, rand_id])
                return JsonResponse({'status': '0', 'message': 'New Card Captured', 'data': [{'name': 'New Card'}]})
            
            stud_id = tag_row[0]
            # Any negative number represents an Unassigned tag!
            is_unassigned = False
            try:
                if int(stud_id) < 0:
                    is_unassigned = True
            except ValueError:
                pass
            if is_unassigned:
                return JsonResponse({'status': '0', 'message': 'Card Not Assigned Yet', 'data': [{'name': 'Unassigned'}]})

            cursor.execute("SELECT name FROM student_register WHERE stud_id = %s", [stud_id])
            student_row = cursor.fetchone()
            student_name = student_row[0] if student_row else "Unknown Student"

            # --- ALWAYS OPEN ACCESS + TRACK APPROVAL LOGIC ---
            
            # 1. Check if they are currently OUT (needs IN)
            cursor.execute("""
                SELECT request_detail_id, status
                FROM gate_pass_details 
                WHERE (roll_no = %s OR stud_id = %s) AND out_time IS NOT NULL AND in_time IS NULL 
                ORDER BY request_date DESC LIMIT 1
            """, [stud_id, stud_id])
            active_out = cursor.fetchone()
            
            # 2. Check if they have an active request waiting to be used (might be Approved, Pending, or Rejected)
            cursor.execute("""
                SELECT request_detail_id, status 
                FROM gate_pass_details 
                WHERE (roll_no = %s OR stud_id = %s) AND out_time IS NULL 
                ORDER BY request_date DESC LIMIT 1
            """, [stud_id, stud_id])
            waiting_out = cursor.fetchone()
            
            current_time = timezone.now()

            if active_out:
                # They are returning to campus! Close out the current pass.
                request_id = active_out[0]
                status_flag = active_out[1] if active_out[1] else 'Unknown'
                cursor.execute("UPDATE gate_pass_details SET in_time = %s WHERE request_detail_id = %s", [current_time, request_id])
                cursor.execute("INSERT INTO gate_pass_history (stud_id, passing_date, passing_time, auth_status) VALUES (%s, CURDATE(), CURTIME(), %s)", [stud_id, status_flag])
                msg = "Returned IN"
                
            elif waiting_out:
                # They are leaving using an existing pass (we don't care if it's Approved or Pending, just mark it OUT!)
                request_id = waiting_out[0]
                status_flag = waiting_out[1] if waiting_out[1] else 'Unknown'
                cursor.execute("UPDATE gate_pass_details SET out_time = %s WHERE request_detail_id = %s", [current_time, request_id])
                cursor.execute("INSERT INTO gate_pass_history (stud_id, passing_date, passing_time, auth_status) VALUES (%s, CURDATE(), CURTIME(), %s)", [stud_id, status_flag])
                msg = "Departed OUT"
                
            else:
                # They are leaving campus entirely without EVER requesting a gate pass!
                cursor.execute("""
                    INSERT INTO gate_pass_details (stud_id, roll_no, reason, request_date, out_time, status)
                    VALUES (%s, %s, 'Unauthorized Campus Exit', %s, %s, 'Not Approved')
                """, [stud_id, stud_id, current_time.date(), current_time])
                cursor.execute("INSERT INTO gate_pass_history (stud_id, passing_date, passing_time, auth_status) VALUES (%s, CURDATE(), CURTIME(), %s)", [stud_id, 'Not Approved'])
                msg = "Departed (No Pass)"

            # BUT ALWAYS physically grant access to open the hardware gate!
            return JsonResponse({'status': '1', 'message': msg, 'data': [{'name': student_name}]})

    return JsonResponse({'status': '0', 'message': 'Invalid method'})



def assign_nfc_tag(request):
    """Admin view to assign an NFC tag UID to a student."""
    if not request.session.get('admin'):
        return redirect('login')

    message = None
    existing_tag = None
    students = []
    unassigned_tags = []

    with connection.cursor() as cursor:
        cursor.execute("SELECT stud_id, name FROM student_register ORDER BY name")
        students = cursor.fetchall()
        cursor.execute("SELECT staff_id, name, staff_type FROM staff_register ORDER BY name")
        staffs = cursor.fetchall()
        # Fetch unassigned recently tapped cards (all negative IDs are unassigned)
        cursor.execute("SELECT tag_uid, assigned_at FROM nfc_tags WHERE stud_id < 0 ORDER BY assigned_at DESC")
        unassigned_tags = cursor.fetchall()

    if request.method == 'POST':
        stud_id = request.POST.get('stud_id', '').strip()
        tag_uid  = request.POST.get('tag_uid',  '').strip()

        if not stud_id or not tag_uid:
            message = ('error', 'Both Student ID and NFC Tag UID are required.')
        else:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT stud_id FROM nfc_tags WHERE tag_uid = %s", [tag_uid]
                )
                conflict = cursor.fetchone()

                conflict_is_assigned = False
                if conflict and str(conflict[0]) != str(stud_id):
                    try:
                        if int(conflict[0]) >= 0:
                            conflict_is_assigned = True
                    except ValueError:
                        conflict_is_assigned = True

                if conflict_is_assigned:
                    message = ('error', f'Tag UID "{tag_uid}" is already assigned to user {conflict[0]}. Remove it first.')
                else:
                    cursor.execute(
                        "SELECT id FROM nfc_tags WHERE stud_id = %s", [stud_id]
                    )
                    existing = cursor.fetchone()

                    # Clean up the unassigned placeholder FIRST to free the UNIQUE tag_uid Key
                    cursor.execute("DELETE FROM nfc_tags WHERE tag_uid = %s AND stud_id < 0", [tag_uid])

                    if existing:
                        cursor.execute(
                            "UPDATE nfc_tags SET tag_uid = %s, assigned_at = NOW() WHERE stud_id = %s",
                            [tag_uid, stud_id]
                        )
                        message = ('success', f'NFC tag updated successfully for student {stud_id}.')
                    else:
                        cursor.execute(
                            "INSERT INTO nfc_tags (tag_uid, stud_id, assigned_at) VALUES (%s, %s, NOW())"
                            " ON DUPLICATE KEY UPDATE stud_id=%s",
                            [tag_uid, stud_id, stud_id]
                        )
                        message = ('success', f'NFC tag assigned successfully to student {stud_id}.')
                        
                    # Re-fetch unassigned tags so they disappear from list instantly
                    cursor.execute("SELECT tag_uid, assigned_at FROM nfc_tags WHERE stud_id < 0 ORDER BY assigned_at DESC")
                    unassigned_tags = cursor.fetchall()

    selected_stud_id = request.GET.get('stud_id') or request.POST.get('stud_id')
    if selected_stud_id:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT tag_uid FROM nfc_tags WHERE stud_id = %s", [selected_stud_id]
            )
            row = cursor.fetchone()
            existing_tag = row[0] if row else None

    return render(request, 'assign_nfc_tag.html', {
        'staffs': staffs,
        'students':    students,
        'unassigned_tags': unassigned_tags,
        'message':     message,
        'existing_tag': existing_tag,
        'selected_stud_id': selected_stud_id,
    })