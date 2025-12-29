# دار جمّال
موقع إلكتروني — قيد التطوير.

## دليل النشر عبر GitHub + Firebase + Cloud Run

هذا المشروع مهيّأ للنشر التلقائي:
- الواجهة (Front-end) على Firebase Hosting.
- الباك (Flask) على Google Cloud Run.
- GitHub Actions يتكفل بالنشر عند كل `push` على فرع `main`.

### 1) إنشاء مستودع GitHub ورفع المشروع
- أنشئ ريبو جديد على GitHub.
- نفّذ الأوامر:
  - `git init`
  - `git add .`
  - `git commit -m "Initial site + backend + CI"`
  - `git branch -M main`
  - `git remote add origin https://github.com/<username>/<repo>.git`
  - `git push -u origin main`

### 2) إعداد Firebase Hosting (الواجهة)
- أنشئ مشروع Firebase: https://console.firebase.google.com/
- حدّث ملف `.firebaserc` بوضع الـ Project ID الحقيقي بدل `mdj-project-id`.
- أضف أسرار (Secrets) داخل إعدادات الريبو على GitHub → Settings → Secrets:
  - `FIREBASE_PROJECT_ID`: معرّف مشروع Firebase.
  - `FIREBASE_SERVICE_ACCOUNT`: محتوى JSON كامل لحساب خدمة Firebase (يفضل صلاحية Firebase Admin).
- ملف `firebase.json` يحتوي `rewrites` لتمرير `/api/**` إلى خدمة Cloud Run لاحقًا.

### 3) إعداد Google Cloud Run (الباك)
- أنشئ مشروع على Google Cloud (يمكن استخدام نفس الـ Project ID).
- فعّل خدمات: Cloud Run, Cloud Build, Artifact Registry.
- أنشئ حساب خدمة (Service Account) للووركفلو مع الصلاحيات التالية:
  - `roles/run.admin`
  - `roles/cloudbuild.builds.editor`
  - `roles/artifactregistry.admin`
  - `roles/storage.admin`
- أضف أسرار إلى GitHub:
  - `GCP_PROJECT_ID`: معرّف مشروع Google Cloud.
  - `GCP_SERVICE_ACCOUNT_KEY`: محتوى JSON لحساب الخدمة أعلاه.

### 4) ربط الاستضافتين سويًا
- حدّث `firebase.json` بقيمة `serviceId` و `region` الفعلية لخدمة Cloud Run (مثال: `mdj-backend` و `us-central1`).
- بعد الـ `push` على `main`:
  - ووركفلو `cloud-run.yml` سيقوم ببناء ونشر الباك.
  - ووركفلو `firebase-hosting.yml` سينشر الواجهة.
- اختبر:
  - واجهة: `https://<your-firebase-app>.web.app/`
  - صحة الباك عبر الواجهة: `https://<your-firebase-app>.web.app/api/health`

### 5) ملاحظات هامة
- قاعدة بيانات SQLite داخل Cloud Run غير دائمة؛ يُنصح باستخدام Cloud SQL أو Firestore إذا أردت بيانات دائمة.
- الاستدعاءات من الواجهة إلى الباك في الإنتاج تمر عبر Firebase Hosting (`/api/**`) فلا تحتاج CORS.
- محليًا، صفحة `news.html` تستدعي `http://127.0.0.1:5501/api/news` إذا كنت تعمل على السيرفر المحلي.

### 6) ضبط دومين مخصص (اختياري)
- من Firebase Hosting: أضف دومينك المخصص واتبع تعليمات إعداد DNS.

### 7) تشغيل محليًا
- الباك: `python backend/app.py` ثم افتح `http://127.0.0.1:5501/api/health`
- الواجهة: عبر خادم بسيط (مثال VS Code Live Server) ثم افتح `http://localhost:5500/index.html`

إذا أحببت، زوّدني بـ `Firebase Project ID` واسم خدمة Cloud Run والمنطقة (region) لأقوم بتحديث الملفات والأسرار اللازمة بنفسي.