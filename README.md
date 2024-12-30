# Probabilistic Reinforcement Learning Task

## Overview
This Python-based experiment implements a probabilistic reinforcement learning task with two phases. The experiment includes a practice phase followed by two experimental phases, where participants make choices between paired stimuli and receive feedback based on their performance. The task uses a monetary reward system to reinforce learning.

## Features
- Practice phase for participant familiarization
- Two distinct experimental phases (learning and extinction phase)
- Real-time feedback and reward system
- Participant data collection and management
- Fullscreen visual stimulus presentation
- Response time tracking
- Automated data saving in Excel format

## Requirements

### Dependencies
- Python 3.x
- tkinter
- pygame
- pandas
- openpyxl (for Excel file handling)

### Required Files
- `stimuli_data.xlsx`: Contains stimulus pairs and correct responses for the first phase
- `ext_stimulus_data.xlsx`: Contains stimulus pairs for the second phase
- `trial_images.xlsx`: Contains practice trial information
- Image files referenced in the Excel files

## Installation
1. Install required Python packages:
```bash
pip install pygame pandas openpyxl tk
```

2. Ensure all required Excel files and image stimuli are in the same directory as the script.

## Usage

### Running the Experiment
1. Execute the main script:
```bash
python experiment_script.py
```

2. Enter participant information in the GUI:
   - Participant Number
   - Gender (1 = Female, 2 = Male)
   - Age
   - Stimulation Condition (1 = tVNS, 2 = Sham)

### Experiment Flow
1. **Practice Phase**
   - Participants complete practice trials
   - Immediate feedback provided
   - Balance updates shown after each trial

2. **Learning Phase**
   - Timed trials (2-second response window)
   - Feedback provided after each response
   - Running balance displayed
   - Data saved as `[participant_id]_first_phase.xlsx`

3. **Extinction Phase**
   - No time limit for responses
   - No feedback provided
   - Data saved as `[participant_id]_second_phase.xlsx`

## Data Collection

### Participant Information
- Saved as `[participant_id]_participant_info.xlsx`
- Includes:
  - Participant Number
  - Gender
  - Age
  - Stimulation Condition

### Trial Data
Each phase saves separate Excel files containing:
- Phase number
- Trial number
- Stimulus presentations (left/right)
- Participant's response
- Reaction time (milliseconds)
- Accuracy
- Optimal/suboptimal choice information
- Group information
- Subject ID

## Controls
- **Left/Right Arrow Keys**: Select stimuli
- **Space Bar**: Progress through instructions
- **Escape Key**: Emergency exit from experiment

## Monetary Reward System
- Correct responses: +0.2 TL
- Incorrect responses: -0.2 TL
- Timeout (no response): -0.2 TL
- Final balance displayed at experiment completion

## Technical Details
- Fullscreen display using pygame
- Randomized stimulus presentation
- Precise reaction time measurement
- Automatic data backup
- Input validation for participant information

## Error Handling
- Validates participant gender and stimulation condition inputs
- Handles timeout scenarios
- Ensures proper data saving before experiment completion

## File Structure
```
project_directory/
├── experiment_script.py
├── stimuli_data.xlsx
├── ext_stimulus_data.xlsx
├── trial_images.xlsx
└── stimuli/
    └── [image files]
```

## Output Files
The experiment generates three Excel files per participant:
1. `[participant_id]_participant_info.xlsx`: Demographic information
2. `[participant_id]_first_phase.xlsx`: Phase 1 trial data
3. `[participant_id]_second_phase.xlsx`: Phase 2 trial data

## Notes
- Ensure all image paths in Excel files are correct relative to the script location
- Back up data files regularly
- Monitor system performance for consistent timing
- Recommended screen resolution: 1920x1080 or higher
