#!/usr/bin/env python3
"""
Simple PDF generation script using selenium webdriver.
Falls back to manual instructions if selenium is not available.
"""
import os
import sys
import time

def try_selenium_pdf():
    """Try to generate PDF using Selenium Chrome WebDriver"""
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.common.print_page_options import PrintOptions
        
        # Setup Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        # Create WebDriver instance
        driver = webdriver.Chrome(options=chrome_options)
        
        # Load the HTML file
        html_path = os.path.abspath("recovery-dharma-inquiries.html")
        driver.get(f"file://{html_path}")
        
        # Wait for page to load
        time.sleep(2)
        
        # Setup print options
        print_options = PrintOptions()
        print_options.page_ranges = ["1-"]  # All pages
        
        # Generate PDF
        pdf_data = driver.print_page(print_options)
        
        # Save PDF
        with open("recovery-dharma-inquiries.pdf", "wb") as file:
            file.write(pdf_data)
        
        driver.quit()
        print("✅ PDF generated successfully using Selenium: recovery-dharma-inquiries.pdf")
        return True
        
    except ImportError:
        print("❌ Selenium not available")
        return False
    except Exception as e:
        print(f"❌ Selenium error: {e}")
        return False

def manual_instructions():
    """Provide manual instructions for PDF generation"""
    html_path = os.path.abspath("recovery-dharma-inquiries.html")
    
    print("\n📄 Manual PDF Generation Instructions:")
    print("="*50)
    print("1. Open your web browser (Chrome, Firefox, Safari, etc.)")
    print(f"2. Navigate to: file://{html_path}")
    print("3. Press Ctrl+P (Cmd+P on Mac) to open the print dialog")
    print("4. Choose 'Save as PDF' as the destination")
    print("5. Set margins to 'Default' or 'Custom' (1 inch top/bottom, 0.75 inch left/right)")
    print("6. Ensure 'Background graphics' or 'Print backgrounds' is enabled")
    print("7. Save the PDF as 'recovery-dharma-inquiries.pdf'")
    print("\n💡 The HTML file includes:")
    print("   • Proper ada3.css styling")
    print("   • Working table of contents links")
    print("   • All 21 weeks of inquiry content")
    print("   • Print-optimized formatting")

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    if not os.path.exists("recovery-dharma-inquiries.html"):
        print("❌ HTML file not found: recovery-dharma-inquiries.html")
        sys.exit(1)
    
    print("🔄 Attempting to generate PDF...")
    
    # Try automated methods
    if try_selenium_pdf():
        return
    
    # Fall back to manual instructions
    manual_instructions()

if __name__ == "__main__":
    main()