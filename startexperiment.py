import tkinter as tk
from tkinter import ttk
import random
import pandas as pd
import pygame
import time
import tkinter.messagebox as messagebox

def load_stimuli_from_excel(file_path):
    """Reads stimuli and correct answers from Excel file."""
    data = pd.read_excel(file_path)
    trials = []
    for _, row in data.iterrows():
        # Görsellerin pozisyonlarını rastgele belirle
        if random.choice([True, False]):
            trials.append({
                'left_img': row['left_img'],
                'right_img': row['right_img'],
                'correct_side': row['correct_side']
            })
        else:
            trials.append({
                'left_img': row['right_img'],
                'right_img': row['left_img'],
                'correct_side': row['correct_side']
            })
    return trials

def save_trial_data_to_excel(participant_data, trial_data, excel_ordered_trials, phase, output_filename):
    """Saves trial data in original order to .xlsx file."""
    ordered_trial_data = []

    stimuli_data = pd.read_excel('stimuli_data.xlsx')
    
    for i in range(len(excel_ordered_trials)):
        trial = trial_data[i]
        excel_trial = excel_ordered_trials[i]
        
        acc = 1 if trial['selected_side'] == trial['correct_side'] else 0

        selected_img = trial['selected_side']
        optml_img = stimuli_data.loc[i, 'optml']  # optml sütunundaki değer
        check_value = 'optimal' if selected_img == optml_img else 'suboptimal'


        ordered_trial_data.append({
            'phase': phase,  # We add phase information
            'left_img': excel_trial['left_img'],
            'right_img': excel_trial['right_img'],
            'correct_side': trial['correct_side'],
            'selected_side': trial['selected_side'],
            'reaction_time_ms': trial['reaction_time_ms'],
            'acc': acc,
            'trial': i + 1,  # trial number
            'group': participant_data['Stimulation Condition'],  # Participant's group
            'subjID': participant_data['Katılımcı No'],  # Participant number
            'check': check_value  # Optimal/suboptimal bilgisi
        })

    df = pd.DataFrame(ordered_trial_data)
    df.to_excel(output_filename, index=False)

def get_participant_choice(screen, timeout=None):
    """It detects which key the participant presses, with a specified timeout."""
    start_time = time.time()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()  # close the experiment with the ESCAPE key
                elif event.key == pygame.K_LEFT:
                    return 'left', time.time() - start_time
                elif event.key == pygame.K_RIGHT:
                    return 'right', time.time() - start_time
        
        if timeout and time.time() - start_time > timeout:
            return 'timeout', None

def show_feedback(screen, font, feedback_text, feedback_color):
    """Displays the feedback message on the screen."""
    feedback_surface = font.render(feedback_text, True, feedback_color)
    feedback_rect = feedback_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    screen.fill((255, 255, 255))
    screen.blit(feedback_surface, feedback_rect)
    pygame.display.flip()
    pygame.time.wait(2000)

def show_instruction_screen(screen, font, instruction_text):
    """Shows the information screen."""
    screen.fill((255, 255, 255))
    
    # center the information message on the screen
    lines = instruction_text.split('\n')
    for i, line in enumerate(lines):
        text_surface = font.render(line, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + i * 40))
        screen.blit(text_surface, text_rect)
    
    pygame.display.flip()

    # Wait participant to press SPACE key
    waiting_for_space = True
    while waiting_for_space:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting_for_space = False  # Close the cycle after pressing SPACE key
                    

def run_practice_phase():
    """training phase to get the participant accustomed to the experiment."""
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption('Alıştırma Aşaması')
    font = pygame.font.Font(None, 36)

    # Excel dosyasını yükle ve ilk 12 satırı al
    excel_file = 'trial_images.xlsx'
    practice_trials = load_stimuli_from_excel(excel_file)
    

    # Bilgilendirme ekranını göster
    show_instruction_screen(screen, font, "Alıştırma aşamasına hoş geldiniz.\nLütfen boşluk tuşuna basarak başlatınız.")
    trial_balance = 0.0


    for trial in practice_trials:
        left_img = pygame.image.load(trial['left_img'])
        right_img = pygame.image.load(trial['right_img'])
        screen.fill((255, 255, 255))
        screen.blit(left_img, (400, 360))
        screen.blit(right_img, (1000, 360))


        balance_text = font.render(f"Bakiyeniz: {trial_balance:.2f} TL", True, (0, 0, 0))
        screen.blit(balance_text, ((screen.get_width() - balance_text.get_width()) // 2, 10))
        pygame.display.flip()
        pygame.display.flip()

        

        # Wait for participant's selection
        selected_side, reaction_time = get_participant_choice(screen, timeout=2)

        # show feedback
        if selected_side == 'timeout':
            feedback_text = "Zaman doldu!"
            feedback_color = (255, 0, 0)
            trial_balance -= 0.2
        elif selected_side == trial['correct_side']:
            feedback_text = "Doğru! 0.2 TL kazandınız."
            feedback_color = (0, 255, 0)
            trial_balance += 0.2
        else:
            feedback_text = "Yanlış! 0.2 TL kaybettiniz."
            feedback_color = (255, 0, 0)
            trial_balance -= 0.2

        show_feedback(screen, font, feedback_text, feedback_color)

    # Show notification screen when the training phase is completed
    show_instruction_screen(screen, font, "Alıştırma aşaması tamamlandı.\nDeneye geçmek için boşluk tuşuna basınız.")
    pygame.quit()


def start_experiment(participant_data, phase):
    """Initiates the first phase of the experiment."""
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption('Deney - Birinci Aşama')
    font = pygame.font.Font(None, 36)

    # Import excel file
    excel_file = 'stimuli_data.xlsx'  
    excel_ordered_trials = load_stimuli_from_excel(excel_file)
    ordered_trials = excel_ordered_trials

    # Information screen
    show_instruction_screen(screen, font, "Hazır olduğunuzda boşluk tuşuna basarak deneye başlayabilirsiniz.")

    experiment_data = []
    balance = 0.0  

    for trial in ordered_trials:
        trial_data = {
            'left_img': trial['left_img'],
            'right_img': trial['right_img'],
            'correct_side': trial['correct_side'],
            'selected_side': None,
            'reaction_time_ms': None
        }

        left_img = pygame.image.load(trial['left_img'])
        right_img = pygame.image.load(trial['right_img'])
        screen.fill((255, 255, 255))
        screen.blit(left_img, (400, 360))
        screen.blit(right_img, (1000, 360))
        
        # show balance on screen
        balance_text = font.render(f"Güncel bakiye: {balance:.2f} TL", True, (0, 0, 0))
        screen.blit(balance_text, ((screen.get_width() - balance_text.get_width()) // 2, 10))
        pygame.display.flip()

        # Wait for participant's selection, 2 seconds time limit
        selected_side, reaction_time = get_participant_choice(screen, timeout=2)
        selected_image = selected_side + '_img'
        foo = trial[selected_image] if selected_side != 'timeout' else foo
        which_image = foo[:foo.rfind('.')]
        trial_data['selected_side'] = which_image
        trial_data['reaction_time_ms'] = f"{reaction_time * 1000:.9f}" if reaction_time else None

        # show feedback
        if selected_side == 'timeout':
            feedback_text = "Zaman doldu!"
            feedback_color = (255, 0, 0)
            balance -= 0.2  
        elif trial['correct_side'] == which_image:
            balance += 0.2
            feedback_text = "Doğru! 0.2 TL kazandınız."
            feedback_color = (0, 255, 0)
        else:
            balance -= 0.2
            feedback_text = "Yanlış! 0.2 TL kaybettiniz."
            feedback_color = (255, 0, 0)

        experiment_data.append(trial_data)

        show_feedback(screen, font, feedback_text, feedback_color)

    # Save trial data with Excel sort
    save_trial_data_to_excel(participant_data, experiment_data, excel_ordered_trials, phase=1, output_filename=f'{participant_data["Katılımcı No"]}_first_phase.xlsx')

    # Inform the participant to move on to the second stage
    show_instruction_screen(screen, font, "Birinci aşama tamamlandı.\nİkinci aşama için boşluk tuşuna basınız.")
    total_balance = balance
    # go second phase

    return total_balance

def start_second_phase(participant_data, total_balance):
    """Initiates the second phase of the experiment."""
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption('Deney - İkinci Aşama')
    font = pygame.font.Font(None, 36)


    # Import excel file
    excel_file = 'ext_stimulus_data.xlsx'  
    excel_ordered_trials = load_stimuli_from_excel(excel_file)

    experiment_data = []

    # Show information screen
    show_instruction_screen(screen, font, "İkinci aşama başlıyor.\nHazır olduğunuzda boşluk tuşuna basınız.")
    
    # wait for the participant to press the SPACE key
    waiting_for_space = True
    while waiting_for_space:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting_for_space = False

    for trial in excel_ordered_trials:
        trial_data = {
            'left_img': trial['left_img'],
            'right_img': trial['right_img'],
            'correct_side': trial['correct_side'],
            'selected_side': None,
            'reaction_time_ms': None
        }

        # uimport the images and show them on the screen
        left_img = pygame.image.load(trial['left_img'])
        right_img = pygame.image.load(trial['right_img'])
        screen.fill((255, 255, 255))
        screen.blit(left_img, (400, 360))
        screen.blit(right_img, (1000, 360))
        pygame.display.flip()

        # wait for the participant's selection (no time limit)
        selected_side, reaction_time = get_participant_choice(screen, timeout=None) 
        selected_image = selected_side + '_img'
        foo = trial[selected_image] if selected_side != 'timeout' else foo
        which_image = foo[:foo.rfind('.')]
        trial_data['selected_side'] = which_image
        trial_data['reaction_time_ms'] = f"{reaction_time * 1000:.9f}" if reaction_time else None

        # no feedback, just save the results
        experiment_data.append(trial_data)

    # Save trial data with Excel sort (different file for second stage)
    save_trial_data_to_excel(participant_data, experiment_data, excel_ordered_trials, phase=2, output_filename=f'{participant_data["Katılımcı No"]}_second_phase.xlsx')
 
    screen.fill((255, 255, 255))
# Thank you text and balance text
    thank_you_text = "Deneye katıldığınız için teşekkür ederiz."
    balance_text = f"Toplam bakiyeniz: {total_balance:.2f} TL"

    thank_you_surface = font.render(thank_you_text, True, (0, 0, 0))
    thank_you_rect = thank_you_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 30))  # İlk satırı biraz yukarı kaydır

    balance_surface = font.render(balance_text, True, (0, 0, 0))
    balance_rect = balance_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 30))  # İkinci satırı biraz aşağı kaydır

    screen.blit(thank_you_surface, thank_you_rect)
    screen.blit(balance_surface, balance_rect)
    pygame.display.flip()
    pygame.time.wait(5000) 
    pygame.quit()

# Collecting Participant Information with GUI Interface
def collect_participant_info():
    def submit_info():
        participant_data = {
            'Katılımcı No': participant_no.get(),
            'Cinsiyet': gender.get(),
            'Yaş': age.get(),
            'Stimulation Condition': stimulation_condition.get()
        }
                # Gender and Stimulation Condition validation
        if participant_data['Cinsiyet'] not in ['1', '2']:
            messagebox.showerror("Hata", "Cinsiyet bilgisi yalnızca '1' veya '2' olabilir.")
            return
        if participant_data['Stimulation Condition'] not in ['1', '2']:
            messagebox.showerror("Hata", "Stimulation Condition yalnızca '1' veya '2' olabilir.")
            return


        participant_id = participant_data['Katılımcı No']
        output_filename = f"{participant_id}_participant_info.xlsx"

        df = pd.DataFrame([participant_data]) 
        df.to_excel(output_filename, index=False)


        root.destroy()  
        run_practice_phase()  
        total_balance = start_experiment(participant_data, phase=1)
        start_second_phase(participant_data, total_balance)  

    # Start Tkinter interface
    root = tk.Tk()
    root.title("Katılımcı Bilgileri")

    tk.Label(root, text="Katılımcı Numarası:").grid(row=0, column=0)
    tk.Label(root, text="Cinsiyet (1 = Kadın, 2 = Erkek):").grid(row=1, column=0)
    tk.Label(root, text="Yaş:").grid(row=2, column=0)
    tk.Label(root, text="Stimulation Condition (1 = tVNS, 2 = Sham):").grid(row=3, column=0)

    # Participant information entry fields
    participant_no = tk.Entry(root)
    gender = tk.Entry(root)
    age = tk.Entry(root)
    stimulation_condition = tk.Entry(root)

    participant_no.grid(row=0, column=1)
    gender.grid(row=1, column=1)
    age.grid(row=2, column=1)
    stimulation_condition.grid(row=3, column=1)

    tk.Button(root, text='Deneyi Başlat', command=submit_info).grid(row=4, column=1, pady=4)

    root.mainloop()

collect_participant_info()

