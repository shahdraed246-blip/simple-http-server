Task 1 - Simple Web Server (ENCS3320)

How to Run:
1. Navigate to Task1/ folder.
2. Run the server: 
   python3 server.py
3. Open your browser and visit:
   http://localhost:5310/

Features:
- English main page (main_en.html)
- Arabic main page (main_ar.html)
- File request pages (T020_1221160_en.html, T020_1221160_ar.html)
- Custom error pages (403, 404)

Testing:
1. Open http://localhost:5310/ → should show main_en.html
2. Open http://localhost:5310/ar → should show main_ar.html
3. Try requesting existing file (notes.txt) → should return it with 200 OK.
4. Try requesting private_doc.txt → should return 403 Forbidden.
5. Try requesting xyz.txt (not existing) → should return 404 Not Found.

