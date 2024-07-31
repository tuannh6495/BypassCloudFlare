from playwright.sync_api import sync_playwright
import os
from twocaptcha import TwoCaptcha

def get_turnstile_token(sitekey, url, api_key):
    if not api_key:
        api_key = os.getenv('APIKEY_2CAPTCHA', api_key)
    
    solver = TwoCaptcha(api_key)
    
    try:
        result = solver.turnstile(
            sitekey=sitekey,
            url=url,
        )
        # Kết quả thường là một từ điển với khóa 'code' chứa token
        return result.get('code')
    except Exception as e:
        print(f"Lỗi khi giải captcha: {e}")
        return None
    

def login_to_batdongsan(phone_number, password):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            
            # Truy cập trang đăng nhập
            page.goto("https://batdongsan.com.vn/sellernet/trang-dang-nhap")
            
            # Đợi để đảm bảo trang đã tải xong
            page.wait_for_load_state("networkidle")

            is_exsist = page.query_selector('xpath=/html/body/div[1]/div/h1')
            if is_exsist is not None:
                token = get_turnstile_token(data_sitekey, page.url, '676e02eae5f1dcc0c26f9c6b1bcddf15')
                if token:
                    print(f"Token Turnstile: {token}")
                else:
                    print("Không thể lấy token.")
            
            # Nhập số điện thoại
            page.fill("input[name=username]", phone_number)
            
            # Nhập mật khẩu
            page.fill("input[name=password]", password)
            
            # Click nút đăng nhập
            page.click("button[id=signin-button]")
            
            # Đợi để trang xử lý đăng nhập
            page.wait_for_load_state("networkidle")

            is_exsist = page.query_selector('xpath=/html/body/div[1]/div/h1')
            if is_exsist is not None:
                token = get_turnstile_token(data_sitekey, page.url, '676e02eae5f1dcc0c26f9c6b1bcddf15')
                if token:
                    print(f"Token Turnstile: {token}")
                else:
                    print("Không thể lấy token.")
            
            # Ở đây bạn có thể thêm các thao tác khác sau khi đăng nhập
            
            # Đóng trình duyệt
            # browser.close()       
    except Exception as e:
        print(f"Lỗi khi giải captcha: {e}")
        return None 


if __name__ == "__main__":
    phone_number = "0975329731"
    password = "Huytuan@123"
    data_sitekey = '0x4AAAAAAADnPIDROrmt1Wwj'

    login_to_batdongsan(phone_number, password)