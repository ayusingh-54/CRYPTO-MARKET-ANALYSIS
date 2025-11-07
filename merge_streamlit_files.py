# =============================================================================
# AUTOMATED INTEGRATION SCRIPT
# Merges all Streamlit continuation parts into one complete application
# =============================================================================

# Instructions:
# 1. Make sure all these files are in the same directory:
#    - streamlit_app_enhanced.py
#    - streamlit_continuation_part1.py
#    - streamlit_continuation_part2.py
#    - streamlit_continuation_part3.py
#
# 2. Run this script in PowerShell from the project directory:
#    python merge_streamlit_files.py
#
# 3. The output will be: streamlit_app_final.py

import os

def merge_files():
    """Merge all Streamlit continuation files into one complete application."""
    
    print("🚀 Starting Streamlit App Integration...")
    print("-" * 60)
    
    # Define file paths
    base_file = "streamlit_app_enhanced.py"
    part1 = "streamlit_continuation_part1.py"
    part2 = "streamlit_continuation_part2.py"
    part3 = "streamlit_continuation_part3.py"
    output_file = "streamlit_app_final.py"
    
    # Check if all files exist
    files_to_check = [base_file, part1, part2, part3]
    for file in files_to_check:
        if not os.path.exists(file):
            print(f"❌ ERROR: {file} not found!")
            return False
    
    print("✅ All source files found")
    
    try:
        # Read base file
        print(f"📖 Reading {base_file}...")
        with open(base_file, 'r', encoding='utf-8') as f:
            base_content = f.read()
        
        # Read continuation parts
        print(f"📖 Reading {part1}...")
        with open(part1, 'r', encoding='utf-8') as f:
            part1_content = f.read()
        
        print(f"📖 Reading {part2}...")
        with open(part2, 'r', encoding='utf-8') as f:
            part2_content = f.read()
        
        print(f"📖 Reading {part3}...")
        with open(part3, 'r', encoding='utf-8') as f:
            part3_content = f.read()
        
        # Clean up continuation parts - remove header comments
        # Part1: Remove everything before the first 'if page' statement
        if "# Common sidebar filters" in part1_content:
            part1_content = "# Common sidebar filters" + part1_content.split("# Common sidebar filters")[1]
        
        # Part2: Remove everything before the first 'if page' statement
        if 'if page == "📊 Advanced Analytics":' in part2_content:
            part2_content = 'if page == "📊 Advanced Analytics":' + part2_content.split('if page == "📊 Advanced Analytics":')[1]
        
        # Part3: Remove everything before "with tabs[1]:" and add proper indentation
        if "with tabs[1]:" in part3_content:
            # Get content starting from "with tabs[1]:"
            part3_lines = part3_content.split('\n')
            start_index = -1
            for i, line in enumerate(part3_lines):
                if 'with tabs[1]:' in line:
                    start_index = i
                    break
            
            if start_index != -1:
                # Keep from this line onwards and ensure proper indentation
                remaining_lines = part3_lines[start_index:]
                # Add 4 spaces to each line that isn't already indented properly
                fixed_lines = []
                for line in remaining_lines:
                    if line.strip().startswith('with tabs['):
                        # This should have 4 spaces
                        fixed_lines.append('    ' + line.lstrip())
                    else:
                        # Keep existing indentation
                        fixed_lines.append(line)
                part3_content = '\n'.join(fixed_lines)
        
        # Create merged content
        print("🔧 Merging files...")
        
        # Find the insertion point in base file (at the "Continue with other pages" section)
        insertion_marker = "# Continue with other pages..."
        
        if insertion_marker in base_content:
            # Split base content at insertion point - keep everything before the marker
            parts = base_content.split(insertion_marker)
            before_marker = parts[0] + insertion_marker + "\n"
            
            # Combine all parts
            merged_content = before_marker
            merged_content += "\n\n# =============================================================================\n"
            merged_content += "# DASHBOARD, ANALYTICS, RISK ANALYSIS, AND DEEP DIVE PAGES\n"
            merged_content += "# Integrated from continuation files\n"
            merged_content += "# =============================================================================\n\n"
            merged_content += part1_content
            merged_content += "\n\n" + part2_content
            merged_content += "\n\n" + part3_content
            
            # Add footer for all pages
            merged_content += """

# =============================================================================
# FOOTER FOR ALL ANALYSIS PAGES
# =============================================================================

if page != "📋 Assignment Details":
    st.markdown("---")
    st.markdown(\"\"\"
    <div style='text-align: center; color: #888; padding: 20px;'>
        <p><b>Bitcoin Trader Performance vs Market Sentiment Dashboard</b></p>
        <p>Created by Ayush Singh | Ayusingh693@gmail.com | +91 7031678999</p>
        <p>Built with Streamlit • Powered by Plotly • Analyzed with Pandas</p>
    </div>
    \"\"\", unsafe_allow_html=True)
"""
            
            # Write to output file
            print(f"💾 Writing to {output_file}...")
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(merged_content)
            
            print("✅ Integration successful!")
            print("-" * 60)
            print(f"📄 Output file created: {output_file}")
            print(f"📏 Total size: {len(merged_content)} characters")
            print(f"📊 Total lines: {len(merged_content.splitlines())}")
            print()
            print("🎉 You can now run the application with:")
            print(f"   streamlit run {output_file}")
            print()
            return True
        else:
            print("❌ ERROR: Could not find insertion marker in base file!")
            return False
    
    except Exception as e:
        print(f"❌ ERROR during merging: {str(e)}")
        return False

if __name__ == "__main__":
    success = merge_files()
    if not success:
        print()
        print("⚠️  Integration failed. Please check the error messages above.")
        print("💡 Tip: Make sure all files are in the same directory and have the correct names.")
