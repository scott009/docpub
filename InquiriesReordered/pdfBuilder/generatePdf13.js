const fs = require('fs-extra');
const path = require('path');
const puppeteer = require('puppeteer');

async function generatePdf() {
    try {
        // Read input files
        const jsonPath = path.join(__dirname, 'reOrdInq13.json');
        const cssPath = path.join(__dirname, 'ada3.css');
        
        const jsonData = await fs.readJson(jsonPath);
        const cssContent = await fs.readFile(cssPath, 'utf-8');

        // Function to render content array
        function renderContent(content) {
            if (!content) return '';
            
            return content.map(item => {
                if (!item) return '';
                
                const classes = item.class ? ` class="${item.class}"` : '';
                const id = item.id ? ` id="${item.id}"` : '';
                
                switch(item.type) {
                    case 'p':
                        return `<p${classes}${id}>${item.text || ''}</p>`;
                    case 'h1':
                    case 'h2':
                    case 'h3':
                    case 'h4':
                    case 'h5':
                    case 'h6':
                        return `<${item.type}${classes}${id}>${item.text || ''}</${item.type}>`;
                    case 'ul':
                    case 'ol':
                        const items = (item.items || []).map(li => {
                            const liClasses = li.class ? ` class="${li.class}"` : '';
                            const liId = li.id ? ` id="${li.id}"` : '';
                            return `<li${liClasses}${liId}>${li.text || ''}</li>`;
                        }).join('');
                        return `<${item.type}${classes}${id}>${items}</${item.type}>`;
                    case 'grounding':
                    case 'aftercare':
                    case 'question':
                        return `<div class="${item.type}"${id}>${item.text || ''}</div>`;
                    default:
                        return item.text ? `<div${classes}${id}>${item.text}</div>` : '';
                }
            }).join('');
        }

        // Function to render sections recursively
        function renderSections(sections, level = 1) {
            if (!sections) return '';
            
            return sections.map(section => {
                if (!section) return '';
                
                const headingLevel = Math.min(6, section.level || level);
                const headingTag = `h${headingLevel}`;
                const sectionClass = section.class ? ` class="${section.class}"` : '';
                const sectionId = section.id ? ` id="${section.id}"` : '';
                
                let html = `
                    <div${sectionClass}${sectionId}>
                        <${headingTag}>${section.heading || ''}</${headingTag}>
                        ${renderContent(section.content)}
                        ${renderSections(section.sections, headingLevel + 1)}
                    </div>
                `;
                
                return html;
            }).join('');
        }

        // Function to convert JSON to HTML with proper structure
        function jsonToHtml(data) {
            let html = '<main>';
            
            // Add title if exists
            if (data.title) {
                const titleClass = data.title.class ? ` class="${data.title.class}"` : '';
                html += `<h1${titleClass}>${data.title.text || ''}</h1>`;
            }
            
            // Render main sections
            if (data.sections && data.sections.length > 0) {
                html += renderSections(data.sections);
            }
            
            // Render footnotes if any
            if (data.footnotes && data.footnotes.length > 0) {
                html += '<div class="footnotes">';
                html += '<h2>Footnotes</h2>';
                html += data.footnotes.map((note, index) => 
                    `<div class="footnote" id="fn-${index + 1}">
                        <a href="#fnref-${index + 1}" class="footnote-backref">↩</a>
                        ${note}
                    </div>`
                ).join('');
                html += '</div>';
            }
            
            html += '</main>';
            return html;
        }

        // Create HTML content
        const htmlContent = `
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>${jsonData.title?.text || 'Inquiry Document'}</title>
            <style>${cssContent}</style>
        </head>
        <body>
            ${jsonToHtml(jsonData)}
        </body>
        </html>
        `;

        // Launch Puppeteer
        const browser = await puppeteer.launch({
            headless: true,
            args: ['--no-sandbox', '--disable-setuid-sandbox']
        });
        
        const page = await browser.newPage();
        
        // Set content and generate PDF
        await page.setContent(htmlContent, { 
            waitUntil: 'networkidle0',
            timeout: 30000
        });
        
        // Generate PDF
        const pdfPath = path.join(__dirname, 'reOrdInq13.pdf');
        
        await page.pdf({
            path: pdfPath,
            format: 'A4',
            printBackground: true,
            margin: {
                top: '20mm',
                right: '20mm',
                bottom: '20mm',
                left: '20mm'
            },
            displayHeaderFooter: false
        });

        console.log(`PDF generated successfully at: ${pdfPath}`);
        
        await browser.close();
    } catch (error) {
        console.error('Error generating PDF:', error);
        process.exit(1);
    }
}

generatePdf();
