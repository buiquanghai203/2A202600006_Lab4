from langchain_core.tools import tool

FLIGHTS_DB = {
    ('Hà Nội', 'Đà Nẵng'):[
        {'airline': 'Vietnam Airlines', 'departure':'06:00', 'arrival':
        '07:20', 'price':1_450_000, 'class':'economy'},
        {'airline': 'Vietnam Airlines', 'departure':'14:00', 'arrival':
        '15:20', 'price':2_800_000, 'class':'business'},
        {'airline': 'Vietjet Air', 'departure':'08:30', 'arrival':
                '09:50', 'price':890_000, 'class':'economy'},
        {'airline': 'Bamboo Airway', 'departure':'11:00', 'arrival':
                '12:20', 'price':1_200_000, 'class':'economy'},

    ],
    ("Hà Nội", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "07:00", "arrival": "09:15", "price": 2_100_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "10:00", "arrival": "12:15", "price": 1_350_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "16:00", "arrival": "18:15", "price": 1_100_000, "class": "economy"}
    ],
    ("Hà Nội", "Hồ Chí Minh"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "08:10", "price": 1_600_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "07:30", "arrival": "09:40", "price": 950_000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "12:00", "arrival": "14:10", "price": 1_300_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "18:00", "arrival": "20:10", "price": 3_200_000, "class": "business"}
    ],
    ("Hồ Chí Minh", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "09:00", "arrival": "10:20", "price": 1_300_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "13:00", "arrival": "14:20", "price": 780_000, "class": "economy"}
    ],
    ("Hồ Chí Minh", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "08:00", "arrival": "09:00", "price": 1_100_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "15:00", "arrival": "16:00", "price": 650_000, "class": "economy"}
    ]
}
HOTELS_DB = {
    "Đà Nẵng": [
        {"name": "Mường Thanh Luxury", "stars": 5, "price_per_night": 1_800_000, "area": "Mỹ Khê", "rating": 4.5},
        {"name": "Sala Danang Beach", "stars": 4, "price_per_night": 1_200_000, "area": "Mỹ Khê", "rating": 4.3},
        {"name": "Fivitel Danang", "stars": 3, "price_per_night": 650_000, "area": "Sơn Trà", "rating": 4.1},
        {"name": "Memory Hostel", "stars": 2, "price_per_night": 250_000, "area": "Hải Châu", "rating": 4.6},
        {"name": "Christina's Homestay", "stars": 2, "price_per_night": 350_000, "area": "An Thượng", "rating": 4.7}
    ],
    "Phú Quốc": [
        {"name": "Vinpearl Resort", "stars": 5, "price_per_night": 3_500_000, "area": "Bãi Dài", "rating": 4.4},
        {"name": "Sol by Meliá", "stars": 4, "price_per_night": 1_500_000, "area": "Bãi Trường", "rating": 4.2},
        {"name": "Lahana Resort", "stars": 3, "price_per_night": 800_000, "area": "Dương Đông", "rating": 4.0},
        {"name": "9Station Hostel", "stars": 2, "price_per_night": 200_000, "area": "Dương Đông", "rating": 4.5}
    ],
    "Hồ Chí Minh": [
        {"name": "Rex Hotel", "stars": 5, "price_per_night": 2_800_000, "area": "Quận 1", "rating": 4.3},
        {"name": "Liberty Central", "stars": 4, "price_per_night": 1_400_000, "area": "Quận 1", "rating": 4.1},
        {"name": "Cochin Zen Hotel", "stars": 3, "price_per_night": 550_000, "area": "Quận 3", "rating": 4.4},
        {"name": "The Common Room", "stars": 2, "price_per_night": 180_000, "area": "Quận 1", "rating": 4.6}
    ]
}

def format_price(amount: int) -> str:
    """Format giá tiền có dấu chấm phân cách, ví dụ: 1.450.000đ"""
    return f"{amount:,.0f}đ".replace(",", ".")

@tool
def search_flights(origin: str, destination: str) -> str:
    """Tìm chuyến bay từ giữa hai thành phố
       Tham số:
       - origin: thành phố khởi hành (VD: 'Hà Nội', 'Hồ Chí Minh')
       - destination: thành phố đến (VD: 'Đà Nẵng', 'Phú Quốc')
       Trả về danh sách chuyến bay với hãng, giờ bay, giá vé.
       Nếu không tìm thấy tuyến bay, trả về thông báo không có chuyến.
    """
    # Tra cứu FLIGHTS_DB với key (origin, destination)
    key = (origin, destination)
    reverse_key = (destination, origin)
    reversed_direction = False

    if key in FLIGHTS_DB:
        flights = FLIGHTS_DB[key]
    elif reverse_key in FLIGHTS_DB:
        flights = FLIGHTS_DB[reverse_key]
        reversed_direction = True
    else:
        return f"Không tìm thấy chuyến bay từ {origin} đến {destination}."

    # Format danh sách chuyến bay dễ đọc
    if reversed_direction:
        header = f"✈️ Chuyến bay từ {origin} đến {destination}\n"
        header += f"(Dữ liệu tham khảo từ chiều {destination} → {origin})\n"
    else:
        header = f"✈️ Chuyến bay từ {origin} đến {destination}\n"

    header += f"Tìm thấy {len(flights)} chuyến:\n"
    header += "-" * 40 + "\n"

    result = header
    for i, f in enumerate(flights, 1):
        result += f"{i}. {f['airline']} | {f['departure']} → {f['arrival']}"
        result += f" | {f['class'].upper()} | {format_price(f['price'])}\n"

    return result
@tool
def search_hotels(city: str, max_price_per_night: int = 99999999) -> str:
    """
    Tìm kiếm khách sạn tại một thành phố, có thể lọc theo giá tối đa mỗi đêm.
    Tham số:
    - city: tên thành phố (VD: 'Đà Nẵng', 'Phú Quốc', 'Hồ Chí Minh')
    - max_price_per_night: giá tối đa mỗi đêm (VNĐ), mặc định không giới hạn
    Trả về danh sách khách sạn phù hợp với tên, số sao, giá, khu vực, rating.
    """
    # Tra cứu HOTELS_DB
    if city not in HOTELS_DB:
        return f"Không tìm thấy khách sạn tại {city}. Các thành phố hỗ trợ: {', '.join(HOTELS_DB.keys())}"

    # Lọc theo max_price_per_night
    filtered = [h for h in HOTELS_DB[city] if h["price_per_night"] <= max_price_per_night]

    if not filtered:
        return (f"Không tìm thấy khách sạn tại {city} với giá dưới "
                f"{format_price(max_price_per_night)}/đêm. Hãy thử tăng ngân sách.")

    # Sắp xếp theo rating giảm dần
    filtered.sort(key=lambda h: h["rating"], reverse=True)

    # Format đẹp
    result = f"🏨 Khách sạn tại {city}"
    if max_price_per_night < 99999999:
        result += f" (giá dưới {format_price(max_price_per_night)}/đêm)"
    result += f"\nTìm thấy {len(filtered)} kết quả:\n"
    result += "-" * 40 + "\n"

    for i, h in enumerate(filtered, 1):
        stars = "⭐" * h["stars"]
        result += (f"{i}. {h['name']} {stars}\n"
                   f"   Giá: {format_price(h['price_per_night'])}/đêm | "
                   f"Khu vực: {h['area']} | Rating: {h['rating']}/5\n")

    return result

@tool
def calculate_budget(total_budget: int, expenses: str) -> str:
    """
    Tính toán ngân sách còn lại sau khi trừ các khoản chi phí.
    Tham số:
    - total_budget: tổng ngân sách ban đầu (VNĐ)
    - expenses: chuỗi mô tả các khoản chi, mỗi khoản cách nhau bởi dấu phẩy, 
      định dạng 'tên_khoản:số_tiền' (VD: 'vé_máy_bay:890000,khách_sạn:650000')
    Trả về bảng chi tiết các khoản chi và số tiền còn lại. 
    Nếu vượt ngân sách, cảnh báo rõ ràng số tiền thiếu.
    """
    # Parse chuỗi expenses thành dict {tên: số_tiền}
    expense_dict = {}
    try:
        items = expenses.split(",")
        for item in items:
            item = item.strip()
            if not item:
                continue
            if ":" not in item:
                return (f"Lỗi format: '{item}' không đúng định dạng. "
                        f"Vui lòng dùng 'tên_khoản:số_tiền' (VD: 'vé_máy_bay:890000').")
            name, amount_str = item.rsplit(":", 1)
            name = name.strip().replace("_", " ").title()
            amount = int(amount_str.strip())
            expense_dict[name] = amount
    except ValueError:
        return ("Lỗi: Số tiền không hợp lệ. Vui lòng nhập số nguyên. "
                "VD: 'vé_máy_bay:890000,khách_sạn:650000'")

    # Tính tổng chi phí
    total_expenses = sum(expense_dict.values())

    # Tính số tiền còn lại
    remaining = total_budget - total_expenses

    # Format bảng chi tiết
    result = "💰 Bảng chi phí:\n"
    for name, amount in expense_dict.items():
        result += f"  - {name}: {format_price(amount)}\n"
    result += "-" * 30 + "\n"
    result += f"Tổng chi: {format_price(total_expenses)}\n"
    result += f"Ngân sách: {format_price(total_budget)}\n"

    if remaining >= 0:
        result += f"✅ Còn lại: {format_price(remaining)}\n"
    else:
        result += f"⚠️ Vượt ngân sách {format_price(abs(remaining))}! Cần điều chỉnh.\n"

    return result

# --- KẾT THÚC CODE tools.py ---

# Chú ý:
# - search_flights: phải xử lý tuple key, thử tra ngược chiều
# - search_hotels: phải lọc + sắp xếp, không chỉ lookup
# - calculate_budget: phải parse chuỗi, xử lý lỗi, tính toán thực sự
# - 3 tools có MỐI LIÊN HỆ: kết quả flights -> input cho budget -> quyết định hotels
