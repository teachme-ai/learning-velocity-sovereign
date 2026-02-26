import csv
import random
import os

def generate_edtech_data(num_rows=50):
    data = []
    modules = ['MOD-101 (Intro)', 'MOD-201 (Algorithms)', 'MOD-301 (Data Structures)', 'MOD-401 (AI Basics)']
    
    for i in range(num_rows):
        student_id = f"STU-{random.randint(1000, 9999)}"
        course_module = random.choice(modules)
        
        is_dirty = random.random() < 0.2  # 20% chance of outliers
        
        if is_dirty:
            # Negative time or astronomically high score
            if random.random() < 0.5:
                time_spent = random.randint(-120, -10)
                score = random.randint(0, 100)
            else:
                time_spent = random.randint(10, 300)
                score = random.randint(150, 999)
        else:
            time_spent = random.randint(10, 300)
            score = random.randint(0, 100)
            
        data.append({
            'Student_ID': student_id,
            'Course_Module': course_module,
            'Time_Spent': time_spent,
            'Score': score
        })
        
    return data

if __name__ == '__main__':
    header = ['Student_ID', 'Course_Module', 'Time_Spent', 'Score']
    data = generate_edtech_data(50)
    
    base_dir = os.path.abspath(os.path.dirname(__file__))
    output_dir = os.path.join(base_dir, '../data')
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, 'student_logs.csv')
    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(data)
        
    print(f"Successfully generated 50 rows of synthetic EdTech data to {output_file}")
