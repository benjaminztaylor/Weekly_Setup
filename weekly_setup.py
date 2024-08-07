import os
import shutil
from datetime import datetime, timedelta
import click

@click.command()
@click.option('--include-workdays', is_flag=True, help='Include Workdays in the folders')
@click.option('--include-weekend', is_flag=True, help='Include weekend days (Saturday and Sunday) in the folders')
@click.option('--copies', default=1, prompt="Number of template copies", help='The number of template copies (default=1)')
def main(include_workdays, include_weekend, copies):
    this_week, days_to_include = get_days_to_include(include_workdays, include_weekend)
    templates_dir = "Templates"
    week_parent = f"Weeks/Week_{this_week}"
    templates_to_include = select_template_files('Select templates to copy', [f'{template_file}' for template_file in os.listdir(templates_dir)])
    create_folders_and_copies(copies, templates_to_include, days_to_include, templates_dir, week_parent)

def get_days_to_include(include_workdays, include_weekend):
    todays_date = datetime.now()
    todays_day = todays_date.weekday()
    this_week = todays_date.isocalendar().week
    weekend_days = [5, 6]
    
    if todays_day in weekend_days:
        include_weekend = True

    if not include_workdays or todays_day == 6:
        last_day = todays_day
    elif include_workdays and not include_weekend:
        last_day = 4
    else:
        last_day = 6

    days_to_include = [todays_date + timedelta(days=i-todays_day) for i in range(todays_day, last_day+1)]
    return this_week, days_to_include

def create_folders_and_copies(num_copies, templates_to_include, days_to_include, templates_dir, week_parent):
    for day in days_to_include:
        today = day.strftime("%m_%d_%Y")
        new_folder_path = os.path.join(week_parent, today)
        os.makedirs(new_folder_path, exist_ok=True)

        for template_file in templates_to_include:
            template_file_path = os.path.join(templates_dir, template_file)

            for i in range(1, num_copies + 1):
                new_file_name = f"{os.path.splitext(template_file)[0]}_{i}{os.path.splitext(template_file)[1]}"
                new_file_path = os.path.join(new_folder_path, new_file_name)
                shutil.copy(template_file_path, new_file_path)
                print(f"Copied {template_file} to {new_file_path}")

def select_template_files(message, choices):
    click.echo(f"{message}: ")
    for i, choice in enumerate(choices, start=1):
        click.echo(f"{i}. {choice}")
    selection = click.prompt('Enter the numbers of your selection separated by commas', type=str)
    templates_to_include = [choices[int(i) - 1] for i in selection.split(',')]
    return templates_to_include

if __name__ == "__main__":
    main()