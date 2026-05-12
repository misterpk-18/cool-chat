import os
import re

templates_dir = 'templates'
css_dir = os.path.join(templates_dir, 'css')
js_dir = os.path.join(templates_dir, 'js')

os.makedirs(css_dir, exist_ok=True)
os.makedirs(js_dir, exist_ok=True)

files_to_process = ['home.html', 'login.html', 'profile.html', 'signup.html']

for filename in files_to_process:
    filepath = os.path.join(templates_dir, filename)
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        continue
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Extract style
    style_pattern = re.compile(r'<style>(.*?)</style>', re.DOTALL | re.IGNORECASE)
    styles = style_pattern.findall(content)
    
    # Extract script
    script_pattern = re.compile(r'<script>(.*?)</script>', re.DOTALL | re.IGNORECASE)
    scripts = script_pattern.findall(content)
    
    basename = os.path.splitext(filename)[0]
    
    # Create CSS
    if styles:
        css_path = os.path.join(css_dir, f'{basename}.css')
        with open(css_path, 'w', encoding='utf-8') as f:
            f.write(styles[0].strip())
        content = style_pattern.sub(f'<link rel="stylesheet" href="css/{basename}.css">', content, count=1)
        # Remove subsequent style tags if any
        content = style_pattern.sub('', content)
        
    # Create JS
    if scripts:
        js_path = os.path.join(js_dir, f'{basename}.js')
        with open(js_path, 'w', encoding='utf-8') as f:
            f.write(scripts[0].strip())
        content = script_pattern.sub(f'<script src="js/{basename}.js"></script>', content, count=1)
        # Remove subsequent script tags if any
        content = script_pattern.sub('', content)
        
    # Write back the HTML
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
print("Successfully split HTML, CSS, and JS files.")
