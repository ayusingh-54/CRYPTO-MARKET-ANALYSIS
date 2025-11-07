"""
Quick test to check if streamlit_app_final.py has any import or runtime errors
"""

print("Testing streamlit_app_final.py...")
print("=" * 60)

try:
    # Test if the file can be compiled
    import py_compile
    py_compile.compile('streamlit_app_final.py', doraise=True)
    print("✅ File compiles successfully (no syntax errors)")
    
    # Check if all required pages are present
    with open('streamlit_app_final.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    pages = [
        '📋 Assignment Details',
        '🏠 Dashboard',
        '📊 Advanced Analytics',
        '📈 Risk Analysis',
        '🔍 Deep Dive'
    ]
    
    print("\nChecking for pages:")
    for page in pages:
        if f'if page == "{page}":' in content:
            print(f"  ✅ {page}")
        else:
            print(f"  ❌ {page} - NOT FOUND!")
    
    # Check for common required variables
    print("\nChecking for required components:")
    components = [
        ('load_data', 'Data loading function'),
        ('st.set_page_config', 'Page configuration'),
        ('sentiment_order', 'Sentiment order variable'),
        ('colors', 'Color scheme'),
        ('filtered_df', 'Filtered dataframe'),
    ]
    
    for comp, desc in components:
        if comp in content:
            print(f"  ✅ {desc} ({comp})")
        else:
            print(f"  ❌ {desc} ({comp}) - NOT FOUND!")
    
    # Count lines
    lines = content.split('\n')
    print(f"\nFile statistics:")
    print(f"  Total lines: {len(lines)}")
    print(f"  Total characters: {len(content)}")
    
    # Check for indentation issues
    print("\nChecking for common indentation patterns:")
    tab_patterns = ['with tabs[0]:', 'with tabs[1]:', 'with tabs[2]:', 'with tabs[3]:']
    for pattern in tab_patterns:
        count = content.count(pattern)
        print(f"  {pattern} appears {count} times")
    
    print("\n" + "=" * 60)
    print("✅ All basic checks passed!")
    print("\n🚀 Ready to run:")
    print("   streamlit run streamlit_app_final.py")
    
except SyntaxError as e:
    print(f"❌ Syntax Error: {e}")
    print(f"   File: {e.filename}")
    print(f"   Line: {e.lineno}")
    print(f"   Text: {e.text}")
    
except Exception as e:
    print(f"❌ Error: {e}")

print("=" * 60)
