
# Kivy-Snake-Game
&nbsp;&nbsp;&nbsp;&nbsp;🐍 เกมงูคลาสสิก สร้างด้วย Python และเฟรมเวิร์ค Kivy  

---

## สารบัญ  
1. [คำอธิบายเกม](#%E0%B8%84%E0%B8%B3%E0%B8%AD%E0%B8%98%E0%B8%B4%E0%B8%9A%E0%B8%B2%E0%B8%A2%E0%B9%80%E0%B8%81%E0%B8%A1)
2. [การติดตั้ง](#%E0%B8%81%E0%B8%B2%E0%B8%A3%E0%B8%95%E0%B8%B4%E0%B8%94%E0%B8%95%E0%B8%B1%E0%B9%89%E0%B8%87) 
3. [วิธีการเล่น](#%E0%B8%A7%E0%B8%B4%E0%B8%98%E0%B8%B5%E0%B8%81%E0%B8%B2%E0%B8%A3%E0%B9%80%E0%B8%A5%E0%B9%88%E0%B8%99)
4. [คุณสมบัติ](#%E0%B8%84%E0%B8%B8%E0%B8%93%E0%B8%AA%E0%B8%A1%E0%B8%9A%E0%B8%B1%E0%B8%95%E0%B8%B4)
5. [ปุ่มควบคุม](#%E0%B8%9B%E0%B8%B8%E0%B9%88%E0%B8%A1%E0%B8%84%E0%B8%A7%E0%B8%9A%E0%B8%84%E0%B8%B8%E0%B8%A1)  
6. [ตั้งค่า](#%E0%B8%95%E0%B8%B1%E0%B9%89%E0%B8%87%E0%B8%84%E0%B9%88%E0%B8%B2)  
7. [ผู้พัฒนา](#%E0%B8%9C%E0%B8%B9%E0%B9%89%E0%B8%9E%E0%B8%B1%E0%B8%92%E0%B8%99%E0%B8%B2)

---

## คำอธิบายเกม  
สัมผัสประสบการณ์เกมงูคลาสสิกในรูปแบบโมเดิร์น! พร้อมฟีเจอร์ใหม่ล่าสุด:  
- การเคลื่อนไหวของงูที่ลื่นไหล 🌀  
- ระดับความยากที่ปรับได้ 🎚️  
- เอฟเฟกต์เสียงและเพลงประกอบ 🔊  
- ระบบคะแนนแบบไดนามิก 🏆  
- อินเทอร์เฟซผู้ใช้สมัยใหม่ 📱  

---

## การติดตั้ง  
**ขั้นตอนที่ 1:** ติดตั้งโปรแกรมที่จำเป็น  

**1.1 ติดตั้ง Chocolatey (ถ้ายังไม่มี)**  
---เปิด **PowerShell** ด้วยสิทธิ์ Administrator แล้วรัน:
```bash
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```
**1.2 ติดตั้ง Python 3.13.2 ด้วย Chocolatey**
```bash
choco install python --version=3.13.2 -y
```
**1.3 ตรวจสอบเวอร์ชัน**
```bash
python --version
```
**1.4 ติดตั้งเฟรมเวิร์ค Kivy**
```bash
pip install kivy
```
**ขั้นตอนที่ 2:** ดาวน์โหลดเกม
```bash
git clone https://github.com/w-kaewthorn14/kivy-snake.git
cd snake.py
```
## วิธีการเล่น
```bash
#รันคำสั่งนี้เพื่อเริ่มเกม
python snake.py
```

1.  **เป้าหมาย:**  ทำให้งูยาวขึ้นโดยกินอาหาร และหลีกเลี่ยงการชนกำแพงหรือตัวงูเอง
    
2.  **การพัฒนาเกม:**
    
    -   ได้ 1 คะแนนต่ออาหาร 1 ชิ้น 🍎
        
    -   เลเวลอัพทุก 5 คะแนน 🆙
        
    -   ความเร็วเพิ่มขึ้นในแต่ละเลเวล ⚡
        
3.  **ชัยชนะ:**  ไม่มีจุดสิ้นสุด - พยายามทำคะแนนให้สูงที่สุด!
## คุณสมบัติ

-   🎨 อินเทอร์เฟซกราฟิกสมัยใหม่พร้อมเท็กซ์เจอร์
    
-   🎛️ ปรับระดับเสียงได้
    
-   ⏯️ เริ่มเกมใหม่ได้ ( กดปุ่ม p )
    
-   🕒 นาฬิกานับเวลาและสถิติเกม
    
-   🥇 บันทึกคะแนนสูงสุด
    
-   🌟 ระดับความยาก สามารถเลือกได้ในหน้า setting:
    
    -   Easy
        
    -   Medium
        
    -   Hard
## ปุ่มควบคุม

### ปุ่ม&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;การทำงาน
&nbsp;↑&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;เลื่อนขึ้น<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|<br>
&nbsp;↓&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;เลื่อนลง<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|<br>
&nbsp;←&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;เลื่อนซ้าย<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|<br>
&nbsp;→&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;เลื่อนขวา<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|<br>
&nbsp;P&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;เริ่มเกมใหม่/กลับหน้าหลัก<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|<br>
&nbsp;ESC&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ออกเกม<br>
<u>------------------------------------------------</u><br>
## ตั้งค่า

เข้าถึงได้จากเมนูหลัก:
1. **Start Game**
2. **Setting**
**กลับหน้าเมนูหลัก:** เพื่อกลับหน้าแรก
**Volume:**  ใช้สไลด์ปรับระดับเสียงหลัก
**Difficulty Level:**
    
    -   Easy: เหมาะสำหรับผู้เริ่มต้น
        
    -   Medium: ความท้าทายสมดุล
        
    -   Hard: สำหรับมืออาชีพ
3. **Exit**
## ผู้พัฒนา

-   **Developer:**  
	6710110246 นายปรัชญา วัฒนาศรีโรจน์ และ 6710110391 นายวีรภัทร แก้วทอน
    
-   **Framwork:**  ทีม Kivy
    

----------

_© 2024 ทีมพัฒนา Kivy-Snake-Game สงวนลิขสิทธิ์._

[กลับสู่ด้านบน](#kivy-snake-game)
    
