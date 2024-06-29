import re
from .models import SinhVien,GiangVien
def strong_password(password):
    if (
        len(password) >= 8
        and any(c.isupper() for c in password)
        and any(c.islower() for c in password)
        and any(c.isdigit() for c in password)
        and any(c in r'!@#$%^&*()-_=+[]{}|;:,.<>?/"`~' for c in password)
    ):
        return True
    else:
        return False
    
def validate_email(email):
    if re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return True
    else:
        return False

def validate_phone(phone):
    if re.match(r"0\d{9}", phone):
        return True
    else:
        return False
    
def obj_update(obj, validated_data):
    for key, value in validated_data.items():
        setattr(obj, key, value)
    obj.save()
    
def validate_to_update(obj, data):
    errors = {}
    immutable_fields = ['Msv','Role']
    date_fields = ['NgaySinh', 'NgapCapCCCD']

    for key in data:
        value = data[key]
        if key in immutable_fields:
            errors[key] = f"{key} not allowed to change"
        if key in date_fields:
            try:
                day, month, year = map(int, value.split('/'))
                data[key] = f"{year:04d}-{month:02d}-{day:02d}"
            except (ValueError, IndexError):
                errors[key] = f"Invalid date format for {key}. It must be in dd/mm/yyyy format."
    return errors

def role_member(id):
    if SinhVien.objects.filter(Msv=id).exists():
        return "sv"
    elif GiangVien.objects.filter(MaGV=id).exists():
        return "gv"
    else:
        return None
    