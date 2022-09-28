import os
import sys
import pandas as pd


def choose_dir():
    # choosing the current directory if no directory specified #
    if len(sys.argv) == 1:
        directory = "."
    # making sure the given directory is a valid one #
    elif len(sys.argv) == 2:
        directory = sys.argv[1]
        if not os.path.isdir(directory):
            sys.exit("Please check the spelling of your directory. It seems like it doesnt exist")
    return directory

# this function will convert csv representation of mins to int value #
#     for example: "300 mins" (type: str) ====> 300 (type: int)      #
def fixed_minutes(time_string_format):
    return int(time_string_format[:time_string_format.index(" ")])

# this function will scan all the mins in the file and return the biggest #
#        I will assume the biggest duration is the class duration         #
def class_time_calc(all_durations):
    max_value = 0
    for duration in all_durations:
        fixed_duration = fixed_minutes(duration)
        if fixed_duration >= max_value:
            max_value = fixed_duration
    return max_value

def in_emails(this_email, emails_so_far):
    for email in emails_so_far:
        try:
            email1 = email[:email.index("@")]
            if this_email[:4] == email1[:4]:
                return email
            if is_similar(this_email[:this_email.index("@")], email1):
                return email
        except:
            continue
    return False

def is_similar(s1, s2):
    same_letters = 0
    diff_letters = 0
    for char in s1:
        if char in s2:
            same_letters += 1
        else:
            diff_letters += 1
    for char in s2:
        if char in s1:
            same_letters += 1
        else:
            diff_letters += 1
    similarity = same_letters / (len(s1)+len(s2))
    # I will consider 90% of the letters are the same as its the same person #
    if similarity >= 0.90:
        return True
    return False


def main_function(directory):
    summary_list = [{}]
    all_classes_durations = 0
    # scan all directories in
    list_of_used_emails = []
    num_of_meetings = 0
    for file in os.scandir(os.path.join(directory, "csv_files")):
        if file.name.endswith(".csv"):
            try:
                data = pd.read_csv(file.path)
            except:
                # file is utf-16
                data = pd.read_csv(file.path, encoding="utf-16", sep='\t')
            num_of_meetings += 1
            student_time = {}
            names_dict = {}
            class_time = class_time_calc(data["Attendance Duration"])
            for i, email in enumerate(data['Attendee Email']):
                # if someone logged twice from the same email
                check_email = in_emails(email, student_time)
                if check_email:
                    email_sec_time = fixed_minutes(data['Attendance Duration'][i])
                    # if someone connected with 2 devices at the same time, will take the bigger duration
                    if student_time[check_email] + email_sec_time >= class_time:
                        real_time = max(student_time[check_email], email_sec_time)
                    # if someone disconnected and re-logged
                    else:
                        real_time = student_time[check_email] + email_sec_time
                    real_email = in_emails(check_email, list_of_used_emails)
                    if real_email:
                        student_time.update({real_email: int(real_time)})
                        list_of_used_emails.append(real_email)
                    else:
                         student_time.update({check_email: int(real_time)})
                         list_of_used_emails.append(check_email)
                else:
                    real_email = in_emails(email, list_of_used_emails)
                    if real_email:
                        student_time.update({real_email: int(fixed_minutes(data['Attendance Duration'][i]))})
                        list_of_used_emails.append(real_email)
                    else:
                         student_time.update({email: int(fixed_minutes(data['Attendance Duration'][i]))})
                         list_of_used_emails.append(email)

                # check if the name is written in English and properly, if it does, lets add it to the summary csv    #
                # if the name is not written in a good format I will just ignore it (no instructions were given here) #
                if (data['Name'][i][0] >= "A" and data['Name'][i][0] <= "z") and not check_email:
                    names_dict.update({email: data['Name'][i]})

            all_classes_durations += class_time
            summary_list.append(student_time)
    try:
        summary_list[0] = names_dict
    except:
        exit("no csv files in the folder")
    # send the summary list to csv #
    summary = pd.DataFrame(summary_list).transpose()
    header_list = ['Name']
    for i in range(len(summary_list)-1):
        header_list.append(f'Meeting {i+1}')
    summary.to_csv('results.csv',  header=header_list,index_label="Email")
    return num_of_meetings


# Make sure we are running on the main script #
if __name__ == "__main__":
    dir = choose_dir()
    main_function(dir)