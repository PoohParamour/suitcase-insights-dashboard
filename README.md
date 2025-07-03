# 🧳 Suitcase Insights Dashboard

📊 Interactive dashboard for analyzing suitcase consumer behavior survey data

## Features

- 🎯 **10 Comprehensive Pages** covering all aspects of consumer analysis
- 📈 **Interactive Visualizations** with Plotly charts
- 🎨 **Modern UI** with gradient themes and Thai font support
- 📱 **Responsive Design** that works on all devices
- 🔍 **Customer Personas** with detailed behavioral analysis

## Pages

1. **ภาพรวม (Overview)** - Key metrics and summary statistics
2. **ข้อมูลประชากรศาสตร์ (Demographics)** - Age, gender, income analysis
3. **ปัจจัยการตัดสินใจ (Decision Factors)** - What influences purchase decisions
4. **ความต้องการผลิตภัณฑ์ (Product Preferences)** - Design and feature preferences
5. **ความอ่อนไหวต่อราคา (Price Sensitivity)** - Price analysis and affordability
6. **ช่องทางการขาย (Sales Channels)** - Preferred shopping platforms
7. **การตลาด (Marketing)** - Marketing channel effectiveness
8. **การรับรู้แบรนด์ (Brand Awareness)** - Brand recognition analysis
9. **ภาพลักษณ์แบรนด์ (Brand Image)** - Brand perception and barriers
10. **บุคลิกภาพลูกค้า (Customer Personas)** - Detailed customer segmentation

## Technology Stack

- **Frontend**: Streamlit
- **Visualization**: Plotly, Matplotlib, Seaborn
- **Data Processing**: Pandas, NumPy
- **Statistics**: SciPy

## Live Demo

🌐 [View Dashboard](https://your-app.streamlit.app)

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run dashboard.py
```

## Data

The dashboard analyzes survey data from 218 respondents with 62 variables covering:
- Demographics (age, gender, income, occupation)
- Purchase behavior and frequency
- Brand awareness and preferences
- Price sensitivity
- Channel preferences
- Marketing effectiveness

---

**Note**: This dashboard presents anonymized survey data for market research purposes.

## ภาพรวม
Dashboard สำหรับแสดงผลการวิเคราะห์ข้อมูลการสำรวจพฤติกรรมผู้บริโภคกระเป๋าเดินทาง สร้างด้วย Streamlit เพื่อความสะดวกในการนำเสนอผลการวิเคราะห์ให้กับลูกค้า

## คุณสมบัติ
- 📊 **ภาพรวม**: แสดงข้อมูลสำคัญและ insights หลัก
- 👥 **ข้อมูลประชากรศาสตร์**: วิเคราะห์ผู้ตอบแบบสำรวจตามเพศ อายุ อาชีพ รายได้
- ⭐ **ปัจจัยการตัดสินใจ**: ความสำคัญของปัจจัยต่างๆ ในการซื้อกระเป๋าเดินทาง
- 🛍️ **ความต้องการผลิตภัณฑ์**: สไตล์ สี ขนาด และประเภทกระเป๋าที่ต้องการ
- 💰 **ความอ่อนไหวต่อราคา**: ช่วงราคาและปัจจัยด้านราคา
- 📱 **ช่องทางการขาย**: แพลตฟอร์มและช่องทางการซื้อที่นิยม

## การติดตั้ง

### 1. Clone โปรเจค
```bash
git clone <repository-url>
cd suitcase-insights-dashboard
```

### 2. ติดตั้ง Dependencies
```bash
pip install -r requirements.txt
```

### 3. เตรียมข้อมูล
ตรวจสอบให้แน่ใจว่าไฟล์ `data/data_renamefinal.csv` อยู่ในตำแหน่งที่ถูกต้อง

### 4. รัน Dashboard
```bash
streamlit run dashboard.py
```

Dashboard จะเปิดใน browser ที่ `http://localhost:8501`

## โครงสร้างไฟล์
```
├── dashboard.py           # ไฟล์หลักของ dashboard
├── requirements.txt       # dependencies
├── README.md             # คู่มือการใช้งาน
├── data/
│   └── data_renamefinal.csv  # ข้อมูลการสำรวจ
└── notebooks/
    └── 1.ipynb          # notebook ต้นฉบับ
```

## การใช้งาน
1. เปิด dashboard ในเบราว์เซอร์
2. ใช้ sidebar เพื่อเลือกหน้าที่ต้องการดู
3. ดู insights และกราฟต่างๆ ในแต่ละหน้า
4. สามารถ interact กับกราฟได้ (zoom, hover, etc.)

## การ Deploy

### Streamlit Cloud (แนะนำ)
1. Push โค้ดขึ้น GitHub
2. ไปที่ [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect กับ GitHub repository
4. Deploy!

### Local Network
หากต้องการให้คนอื่นในเครือข่ายเดียวกันเข้าถึงได้:
```bash
streamlit run dashboard.py --server.address 0.0.0.0
```

## คุณสมบัติพิเศษ
- ✅ รองรับภาษาไทย
- ✅ Responsive design
- ✅ Interactive charts
- ✅ Professional styling
- ✅ Fast loading with caching

## ปัญหาที่อาจพบ
1. **ไม่พบไฟล์ข้อมูล**: ตรวจสอบ path ของไฟล์ `data/data_renamefinal.csv`
2. **Error กับ Thai fonts**: ใช้เบราว์เซอร์ที่รองรับ Google Fonts
3. **Charts ไม่แสดง**: ตรวจสอบ internet connection สำหรับ Plotly

## การปรับแต่ง
สามารถแก้ไขไฟล์ `dashboard.py` เพื่อ:
- เพิ่มกราฟใหม่
- เปลี่ยนสี theme
- เพิ่มหน้าใหม่
- ปรับ layout

## ผู้พัฒนา
สร้างโดย AI Assistant สำหรับการวิเคราะห์ข้อมูลการสำรวจพฤติกรรมผู้บริโภค 