import streamlit as st
import pandas as pd

def calculate_sgpa(subjects_data):
    """Calculate SGPA from subjects data"""
    total_credit_points = 0
    total_credits = 0
    
    for subject in subjects_data:
        credit_points = subject['credit'] * subject['points']
        total_credit_points += credit_points
        total_credits += subject['credit']
    
    if total_credits == 0:
        return 0
    return total_credit_points / total_credits

def calculate_percentage(sgpa):
    """Calculate percentage from SGPA"""
    return (sgpa - 0.75) * 10

st.sidebar.header("Made by Subhadip🔥")
def calculate_ygpa(odd_semester_data, even_semester_data):
    """Calculate YGPA from odd and even semester data"""
    odd_credit_index = sum([subject['credit'] * subject['points'] for subject in odd_semester_data])
    even_credit_index = sum([subject['credit'] * subject['points'] for subject in even_semester_data])
    odd_total_credits = sum([subject['credit'] for subject in odd_semester_data])
    even_total_credits = sum([subject['credit'] for subject in even_semester_data])
    
    total_credit_index = odd_credit_index + even_credit_index
    total_credits = odd_total_credits + even_total_credits
    
    if total_credits == 0:
        return 0
    return total_credit_index / total_credits

def calculate_dgpa(ygpa_data, course_type="4 Year Degree"):
    """Calculate DGPA based on course type"""
    if course_type == "4 Year Degree":
        if len(ygpa_data) >= 4:
            return (ygpa_data[0] + ygpa_data[1] + 1.5 * ygpa_data[2] + 1.5 * ygpa_data[3]) / 4
    elif course_type == "Lateral Entry":
        if len(ygpa_data) >= 3:
            return (ygpa_data[0] + 1.5 * ygpa_data[1] + 1.5 * ygpa_data[2]) / 4
    elif course_type == "3 Year Degree":
        if len(ygpa_data) >= 3:
            return (ygpa_data[0] + ygpa_data[1] + ygpa_data[2]) / 3
    elif course_type == "2 Year Degree":
        if len(ygpa_data) >= 2:
            return (ygpa_data[0] + ygpa_data[1]) / 2
    elif course_type == "1 Year Degree":
        if len(ygpa_data) >= 1:
            return ygpa_data[0]
    
    return 0

def main():
    st.set_page_config(page_title="MAKAUT SGPA/CGPA Calculator", page_icon="📚", layout="wide")
    
    st.title("🎓 MAKAUT B.Tech SGPA, CGPA, YGPA, DGPA & Percentage Calculator")
    st.markdown("---")
    
    # MAKAUT grading system
    st.sidebar.header("MAKAUT Grading System")
    grading_data = {
        'Letter Grade': ['O', 'E', 'A', 'B', 'C', 'D', 'F', 'I'],
        'Points': [10, 9, 8, 7, 6, 5, 2, 2],
        'Percentage Range': ['90-100', '80-89', '70-79', '60-69', '50-59', '40-49', 'Below 40', 'Incomplete']
    }
    grading_df = pd.DataFrame(grading_data)
    st.sidebar.dataframe(grading_df, use_container_width=True)
    
    st.sidebar.markdown("**Formulas:**")
    st.sidebar.markdown("- SGPA = Σ(Grade Point × Credits) / Total Credits")
    st.sidebar.markdown("- YGPA = (Credit Index Odd + Credit Index Even) / Total Credits")
    st.sidebar.markdown("- DGPA = Weighted average of YGPAs")
    st.sidebar.markdown("- Percentage = (SGPA - 0.75) × 10")
    st.sidebar.markdown("- CGPA = Average of all SGPAs")
    
    # Main content
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 SGPA Calculator", "📈 CGPA Calculator", "🎯 YGPA Calculator", "🏆 DGPA Calculator", "ℹ️ About"])
    
    with tab1:
        st.header("Semester Grade Point Average (SGPA) Calculator")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Enter Subject Details")
            
            # Number of subjects
            num_subjects = st.number_input("Number of Subjects", min_value=1, max_value=20, value=5, step=1)
            
            subjects_data = []
            
            for i in range(num_subjects):
                st.markdown(f"**Subject {i+1}**")
                col_a, col_b, col_c = st.columns(3)
                
                with col_a:
                    subject_name = st.text_input(f"Subject Name {i+1}", value=f"Subject {i+1}", key=f"name_{i}")
                
                with col_b:
                    credit = st.number_input(f"Credits {i+1}", min_value=0.5, max_value=10.0, value=3.0, step=0.5, key=f"credit_{i}")
                
                with col_c:
                    grade_points = st.selectbox(
                        f"Grade Points {i+1}",
                        options=[10, 9, 8, 7, 6, 5, 2],
                        index=2,
                        format_func=lambda x: f"{x} ({'O' if x==10 else 'E' if x==9 else 'A' if x==8 else 'B' if x==7 else 'C' if x==6 else 'D' if x==5 else 'F'})",
                        key=f"grade_{i}"
                    )
                
                subjects_data.append({
                    'name': subject_name,
                    'credit': credit,
                    'points': grade_points
                })
                st.markdown("---")
        
        with col2:
            st.subheader("Calculation")
            
            if st.button("Calculate SGPA", type="primary", key="sgpa_calc"):
                sgpa = calculate_sgpa(subjects_data)
                percentage = calculate_percentage(sgpa)
                
                # Display results
                st.success(f"**SGPA: {sgpa:.2f}**")
                st.info(f"**Equivalent Percentage: {percentage:.2f}%**")
                
                # Detailed breakdown
                st.subheader("Detailed Breakdown")
                breakdown_data = []
                total_credits = 0
                total_credit_points = 0
                
                for subject in subjects_data:
                    credit_points = subject['credit'] * subject['points']
                    breakdown_data.append({
                        'Subject': subject['name'],
                        'Credits': subject['credit'],
                        'Grade Points': subject['points'],
                        'Credit Points': credit_points
                    })
                    total_credits += subject['credit']
                    total_credit_points += credit_points
                
                breakdown_df = pd.DataFrame(breakdown_data)
                st.dataframe(breakdown_df, use_container_width=True)
                
                st.markdown(f"**Total Credits: {total_credits}**")
                st.markdown(f"**Total Credit Points: {total_credit_points}**")
    
    with tab2:
        st.header("Cumulative Grade Point Average (CGPA) Calculator")
        
        st.subheader("Enter Semester-wise SGPA")
        
        # For 8 semesters (B.Tech)
        semesters = []
        total_semesters = st.selectbox("Number of Semesters", options=[2, 4, 6, 8], index=3, key="cgpa_sem")
        
        cols = st.columns(4)
        for i in range(total_semesters):
            with cols[i % 4]:
                sgpa = st.number_input(
                    f"Semester {i+1} SGPA",
                    min_value=0.0,
                    max_value=10.0,
                    value=7.0 + (i * 0.1),
                    step=0.01,
                    key=f"cgpa_sem_{i}"
                )
                semesters.append(sgpa)
        
        if st.button("Calculate CGPA", type="primary", key="cgpa_calc"):
            if semesters:
                cgpa = sum(semesters) / len(semesters)
                percentage = calculate_percentage(cgpa)
                
                st.success(f"**CGPA: {cgpa:.2f}**")
                st.info(f"**Equivalent Percentage: {percentage:.2f}%**")
                
                # Display semester-wise data
                sem_data = []
                for i, sgpa in enumerate(semesters):
                    sem_data.append({
                        'Semester': i+1,
                        'SGPA': sgpa,
                        'Percentage': calculate_percentage(sgpa)
                    })
                
                sem_df = pd.DataFrame(sem_data)
                st.subheader("Semester-wise Performance")
                st.dataframe(sem_df, use_container_width=True)
    
    with tab3:
        st.header("Yearly Grade Point Average (YGPA) Calculator")
        
        st.subheader("Odd Semester Subjects")
        odd_num_subjects = st.number_input("Number of Odd Semester Subjects", min_value=1, max_value=15, value=6, step=1, key="odd_subjects")
        
        odd_semester_data = []
        for i in range(odd_num_subjects):
            st.markdown(f"**Odd Semester Subject {i+1}**")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                subject_name = st.text_input(f"Subject Name {i+1}", value=f"Odd Subject {i+1}", key=f"odd_name_{i}")
            with col2:
                credit = st.number_input(f"Credits {i+1}", min_value=0.5, max_value=10.0, value=3.0, step=0.5, key=f"odd_credit_{i}")
            with col3:
                grade_points = st.selectbox(
                    f"Grade Points {i+1}",
                    options=[10, 9, 8, 7, 6, 5, 2],
                    index=2,
                    format_func=lambda x: f"{x} ({'O' if x==10 else 'E' if x==9 else 'A' if x==8 else 'B' if x==7 else 'C' if x==6 else 'D' if x==5 else 'F'})",
                    key=f"odd_grade_{i}"
                )
            
            odd_semester_data.append({
                'name': subject_name,
                'credit': credit,
                'points': grade_points
            })
        
        st.markdown("---")
        st.subheader("Even Semester Subjects")
        even_num_subjects = st.number_input("Number of Even Semester Subjects", min_value=1, max_value=15, value=6, step=1, key="even_subjects")
        
        even_semester_data = []
        for i in range(even_num_subjects):
            st.markdown(f"**Even Semester Subject {i+1}**")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                subject_name = st.text_input(f"Subject Name {i+1}", value=f"Even Subject {i+1}", key=f"even_name_{i}")
            with col2:
                credit = st.number_input(f"Credits {i+1}", min_value=0.5, max_value=10.0, value=3.0, step=0.5, key=f"even_credit_{i}")
            with col3:
                grade_points = st.selectbox(
                    f"Grade Points {i+1}",
                    options=[10, 9, 8, 7, 6, 5, 2],
                    index=2,
                    format_func=lambda x: f"{x} ({'O' if x==10 else 'E' if x==9 else 'A' if x==8 else 'B' if x==7 else 'C' if x==6 else 'D' if x==5 else 'F'})",
                    key=f"even_grade_{i}"
                )
            
            even_semester_data.append({
                'name': subject_name,
                'credit': credit,
                'points': grade_points
            })
        
        if st.button("Calculate YGPA", type="primary", key="ygpa_calc"):
            ygpa = calculate_ygpa(odd_semester_data, even_semester_data)
            percentage = calculate_percentage(ygpa)
            
            st.success(f"**YGPA: {ygpa:.2f}**")
            st.info(f"**Equivalent Percentage: {percentage:.2f}%**")
            
            # Display detailed breakdown
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Odd Semester Breakdown")
                odd_breakdown = []
                odd_total_credits = 0
                odd_total_points = 0
                
                for subject in odd_semester_data:
                    credit_points = subject['credit'] * subject['points']
                    odd_breakdown.append({
                        'Subject': subject['name'],
                        'Credits': subject['credit'],
                        'Grade Points': subject['points'],
                        'Credit Points': credit_points
                    })
                    odd_total_credits += subject['credit']
                    odd_total_points += credit_points
                
                odd_df = pd.DataFrame(odd_breakdown)
                st.dataframe(odd_df, use_container_width=True)
                st.markdown(f"**Odd Semester Total Credits: {odd_total_credits}**")
                st.markdown(f"**Odd Semester Credit Index: {odd_total_points}**")
            
            with col2:
                st.subheader("Even Semester Breakdown")
                even_breakdown = []
                even_total_credits = 0
                even_total_points = 0
                
                for subject in even_semester_data:
                    credit_points = subject['credit'] * subject['points']
                    even_breakdown.append({
                        'Subject': subject['name'],
                        'Credits': subject['credit'],
                        'Grade Points': subject['points'],
                        'Credit Points': credit_points
                    })
                    even_total_credits += subject['credit']
                    even_total_points += credit_points
                
                even_df = pd.DataFrame(even_breakdown)
                st.dataframe(even_df, use_container_width=True)
                st.markdown(f"**Even Semester Total Credits: {even_total_credits}**")
                st.markdown(f"**Even Semester Credit Index: {even_total_points}**")
            
            st.markdown(f"**Total Credits: {odd_total_credits + even_total_credits}**")
            st.markdown(f"**Total Credit Index: {odd_total_points + even_total_points}**")
    
    with tab4:
        st.header("Degree Grade Point Average (DGPA) Calculator")
        
        course_type = st.selectbox(
            "Select Course Type",
            options=["4 Year Degree", "Lateral Entry", "3 Year Degree", "2 Year Degree", "1 Year Degree"],
            index=0
        )
        
        st.subheader("Enter Year-wise YGPA")
        
        if course_type == "4 Year Degree":
            years_needed = 4
        elif course_type == "Lateral Entry":
            years_needed = 3
        elif course_type == "3 Year Degree":
            years_needed = 3
        elif course_type == "2 Year Degree":
            years_needed = 2
        else:  # 1 Year Degree
            years_needed = 1
        
        ygpa_data = []
        cols = st.columns(min(years_needed, 4))
        
        for i in range(years_needed):
            with cols[i % 4]:
                ygpa = st.number_input(
                    f"Year {i+1} YGPA",
                    min_value=0.0,
                    max_value=10.0,
                    value=7.0 + (i * 0.1),
                    step=0.01,
                    key=f"ygpa_{i}"
                )
                ygpa_data.append(ygpa)
        
        if st.button("Calculate DGPA", type="primary", key="dgpa_calc"):
            dgpa = calculate_dgpa(ygpa_data, course_type)
            percentage = calculate_percentage(dgpa)
            
            st.success(f"**DGPA: {dgpa:.2f}**")
            st.info(f"**Equivalent Percentage: {percentage:.2f}%**")
            
            # Display year-wise data
            year_data = []
            for i, ygpa in enumerate(ygpa_data):
                weight = 1.0
                if course_type == "4 Year Degree" and i >= 2:
                    weight = 1.5
                elif course_type == "Lateral Entry" and i >= 1:
                    weight = 1.5
                
                year_data.append({
                    'Year': i+1,
                    'YGPA': ygpa,
                    'Weight': weight,
                    'Weighted YGPA': ygpa * weight,
                    'Percentage': calculate_percentage(ygpa)
                })
            
            year_df = pd.DataFrame(year_data)
            st.subheader("Year-wise Performance")
            st.dataframe(year_df, use_container_width=True)
            
            # Show formula used
            st.subheader("Formula Used")
            if course_type == "4 Year Degree":
                st.latex(r"DGPA = \frac{YGPA_1 + YGPA_2 + 1.5 \times YGPA_3 + 1.5 \times YGPA_4}{4}")
            elif course_type == "Lateral Entry":
                st.latex(r"DGPA = \frac{YGPA_1 + 1.5 \times YGPA_2 + 1.5 \times YGPA_3}{4}")
            elif course_type == "3 Year Degree":
                st.latex(r"DGPA = \frac{YGPA_1 + YGPA_2 + YGPA_3}{3}")
            elif course_type == "2 Year Degree":
                st.latex(r"DGPA = \frac{YGPA_1 + YGPA_2}{2}")
            else:  # 1 Year Degree
                st.latex(r"DGPA = YGPA_1")
    
    with tab5:
        st.header("About MAKAUT Grading System")
        
        st.markdown("""
        ### MAKAUT Grading System Overview
        
        **SGPA Calculation:**
        - SGPA = Total Credit Points / Total Credits
        - Credit Points = Grade Point × Credits for each subject
        
        **YGPA Calculation:**
        - YGPA = (Credit Index Odd Semester + Credit Index Even Semester) / Total Credits
        - Credit Index = Σ(Grade Point × Credits) for each semester
        
        **DGPA Calculation:**
        - **4 Year Degree:** DGPA = (YGPA₁ + YGPA₂ + 1.5×YGPA₃ + 1.5×YGPA₄) / 4
        - **Lateral Entry:** DGPA = (YGPA₁ + 1.5×YGPA₂ + 1.5×YGPA₃) / 4
        - **3 Year Degree:** DGPA = (YGPA₁ + YGPA₂ + YGPA₃) / 3
        - **2 Year Degree:** DGPA = (YGPA₁ + YGPA₂) / 2
        - **1 Year Degree:** DGPA = YGPA₁
        
        **Percentage Conversion:**
        - Percentage = (SGPA - 0.75) × 10
        
        **CGPA Calculation:**
        - CGPA = Average of all Semester SGPAs
        - For 4-year B.Tech: CGPA = (SGPA₁ + SGPA₂ + ... + SGPA₈) / 8
        
        **Grading Scale:**
        """)
        
        st.dataframe(grading_df, use_container_width=True)
        
        st.markdown("""
        **Result Status:**
        - **X**: Not eligible for Semester Promotion/Degree
        - **XP**: Eligible for Promotion with Backlogs  
        - **P**: Passed and Promoted
        
        **Note:** This calculator follows the official MAKAUT grading system and formulas.
        """)

if __name__ == "__main__":
    main()