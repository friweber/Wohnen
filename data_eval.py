import pandas as pd
import numpy as np
import functions
import matplotlib.pyplot as plt
import plot

file_path_var = 'variablen.csv'
file_path_val = 'datensatz.csv'
file_path_quest = 'fragen.csv'

data_var = pd.read_csv(file_path_var, encoding = "utf-16", delimiter = ";")
data_val = pd.read_csv(file_path_val, encoding = "utf-16", delimiter = ";")
data_quest = pd.read_csv(file_path_quest, encoding = "utf-16", delimiter = ";")

#%%
# Convert price and area to numeric
data_val['NT17_01'] = pd.to_numeric(data_val['NT17_01'], errors='coerce')
data_val['NT08_01'] = pd.to_numeric(data_val['NT08_01'], errors='coerce')


#%% Important functions


#%% Statistic for pariticipation
status_val = functions.condition(data_var, "MEANING", "VAR", "NT01")[:-2]
year_val = functions.condition(data_var, "MEANING", "VAR", "NT15")[:-1]


#%% Bar diagram for rent cost per year

means_percent = []
means_nominal = []
for i in range(len(status_val)):
    part_percent = np.nanmean(functions.condition(data_val, "NT06_01", "NT01", i+1, True)-1)
    part_nominal = np.nanmean(functions.condition_int(data_val, "NT17_01", "NT01", i+1, True)-1)
    area = np.nanmean(functions.condition_int(data_val, "NT08_01", "NT01", i+1, True))
    means_percent.append(part_percent)
    means_nominal.append(part_nominal/area)
    

y_pos = np.arange(len(status_val))

plt.barh(y_pos, means_percent, align='center', alpha=0.7, edgecolor='black')
plt.yticks(y_pos, status_val)
plt.xlabel('% des monatlichen Budgets')
plt.title('Mietkosten nach Art der Unterkunft')
plt.tick_params(
    axis='y',
    which='both',  # major und minor ticks
    left=False     # ticks auf der y-Achse (links)
)

ax = plt.gca()
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# Annotate each bar with values from means_nominal
for i, v in enumerate(means_nominal):
    plt.text(means_percent[i]+1, i, str(np.round(v,1)) + "0 € pro m²", color='black', va='center')
plt.tight_layout()
plt.savefig("cost.png", dpi = 250)
plt.show()
#%% Histogram for price per square meter

data_val['ratio'] = data_val['NT17_01'] / data_val['NT08_01']
data_val.loc[data_val['ratio'] > 30, 'ratio'] = 31

plt.figure(figsize=(8, 6))
bins = np.arange(0, 33, 2.5)


# Calculate percentages for each bin
counts, bins = np.histogram(data_val['ratio'].dropna(), bins=bins)
total_counts = np.sum(counts)
percentages = [(counter / total_counts) * 100 for counter in counts]
plt.bar(bins[:-1], percentages, width=np.diff(bins), align='edge', alpha=0.7, edgecolor='black')

# Plot histogram with percentage labels on y-axis
plt.xticks(np.arange(0, 31, 5))
plt.text(33, -0.97, 'über 30', ha='center', va='center')
plt.xlabel('Quadratmeterpreis in €')
plt.ylabel('Anteil in %')
plt.title('Histogram des Quadratmeterpreises')

# Show plot
plt.tight_layout()
plt.savefig("price_area.png", dpi = 250)
plt.show()
#%% Verteilung für Frage zu Kündigung

# Labels for the questions
title = 'Suppose your rental contract is terminated/not renewed.'
item1 = "I would be … worried about finding new accommodation"
awns1 = ["not at all", "extremly"]
item2 = "I would be … worried about finishning my degree on time"
awns2 = ["not at all", "extremly"]
item3 = "I would ... how to defend my rights"
awns3 = ["know", "not know"]
item4 = "It would be ... to find a comparable accomodation"
awns4 = ["easy", "impossible"]

questions = [item1, item2, item3, item4]
awnser = [awns1, awns2, awns3, awns4]
awnser = [item for sublist in awnser for item in sublist]

#colors for the categories
color = ["r", "b", "g", "k", "y"]

quest = "NT07"

# Plotting the lines and markers
plt.figure(figsize=(8, 8*0.68))
for i in range(len(questions)):
    plt.plot([1, 5], [i, i], color='black')  # Line spanning from yes to no
    plt.plot([1, 1], [i+0.05, i-0.05], color='black')
    plt.plot([5, 5], [i+0.05, i-0.05], color='black')
    plt.text(1., i+0.3, questions[i], ha='left', va='center', weight='bold')
    plt.text(0.9, i, awnser[i*2], ha='right', va='center')
    plt.text(5.1, i, awnser[i*2+1], ha='left', va='center')


for j in range(len(status_val)):
    first = np.nanmean(functions.condition(data_val, quest + "_01", "NT01", j+1, False))
    second = np.nanmean(functions.condition(data_val, quest + "_02", "NT01", j+1, False))
    third = np.nanmean(functions.condition(data_val, quest + "_03", "NT01", j+1, False))
    fourth = np.nanmean(functions.condition(data_val, quest + "_04", "NT01", j+1, False))
    averages = [first, second, third, fourth]
    
    for i in range(len(questions)):
        if i == 0:
            plt.scatter(averages[i], i, s=150, color=color[j], marker='o', alpha = 0.7, label = status_val[j])  # Dot for the average
        else:
            plt.scatter(averages[i], i, s=150, color=color[j], marker='o', alpha = 0.7)  # Dot for the average


# Add a vertical line at position 3
plt.axvline(x=3, color='gray', linestyle='--', alpha = 0.4)

# Hide the box
plt.box(on=None)


plt.ylim(-0.5, len(questions) - 0.5)
plt.legend(ncol=5, loc='lower center', bbox_to_anchor=(0.5, 0), fontsize='medium')

# Set x-axis labels
plt.xticks([])
plt.yticks([])


plt.title(title, weight='bold')

# Show plot
plt.tight_layout()
plt.savefig("terminate.png", dpi = 250)
plt.show()
#%% Verteilung für Frage zu Mieterhöhung
item1 = "I would be ... worried about my financial situation"
awns1 = ["not at all", "extremly"]
item2 = "I would be … worried about finishning my degree on time"
awns2 = ["not at all", "extremly"]
item3 = "It would be ... to find a comparable accomodation"
awns3 = ["easy", "impossible"]
item4 = "I would ... how to defend my rights"
awns4 = ["know", "not know"]

# Labels for the questions
questions = [item1, item2, item3, item4]
awnser = [awns1, awns2, awns3, awns4]
awnser = [item for sublist in awnser for item in sublist]
# Averages for the questions

color = ["r", "b", "g", "k", "y"]

distinction = functions.condition(data_var, "MEANING", "VAR", "NT01")[:-2]

# Plotting the lines and markers
plt.figure(figsize=(8, 8*0.68))
for i in range(len(questions)):
    plt.plot([1, 5], [i, i], color='black')  # Line spanning from yes to no
    plt.plot([1, 1], [i+0.05, i-0.05], color='black')
    plt.plot([5, 5], [i+0.05, i-0.05], color='black')
    plt.text(1., i+0.3, questions[i], ha='left', va='center', weight='bold')
    plt.text(0.9, i, awnser[i*2], ha='right', va='center')
    plt.text(5.1, i, awnser[i*2+1], ha='left', va='center')


for j in range(len(status_val)):
    first = np.nanmean(functions.condition(data_val, "NT19_01", "NT01", j+1, False))
    second = np.nanmean(functions.condition(data_val, "NT19_02", "NT01", j+1, False))
    third = np.nanmean(functions.condition(data_val, "NT19_03", "NT01", j+1, False))
    fourth = np.nanmean(functions.condition(data_val, "NT19_04", "NT01", j+1, False))
    averages = [first, second, third, fourth]
    
    for i in range(len(questions)):
        if i == 0:
            plt.scatter(averages[i], i, s=150, color=color[j], marker='o', alpha = 0.7, label = status_val[j])  # Dot for the average
        else:
            plt.scatter(averages[i], i, s=150, color=color[j], marker='o', alpha = 0.7)  # Dot for the average

# Add a vertical line at position 3
plt.axvline(x=3, color='gray', linestyle='--', alpha = 0.4)

# Hide the box
plt.box(on=None)
plt.ylim(-0.5, len(questions) - 0.5)
plt.legend(ncol=5, loc='lower center', bbox_to_anchor=(0.5, 0), fontsize='medium')

# Set x-axis labels
plt.xticks([])
plt.yticks([])
plt.title('Suppose your rent would be increased by 10%', weight='bold')

# Show plot
plt.tight_layout()
plt.savefig("rent_inc.png", dpi = 250)


#%% Befristung nach Wohnsituation
plot.position_plot_single(8, 7, [1,2,3,4,5,6], data_var, data_val, data_quest)
plt.savefig("befristung.png", dpi = 250)
plt.show()

#%% Wichtigkeit des guten Wohnens nach Wohnsituation
plot.position_plot_single(23, 7, [1,2,3,4,5,6], data_var, data_val, data_quest)
plt.savefig("befristung.png", dpi = 250)
plt.show()
#%% Anfahrtszeit
plot.plot_hist(11, data_var, data_val, data_quest)
plt.show()
plt.savefig("time_to_uni.png", dpi = 250)
#%% Teilnehmenden Status
plot.plot_hist(7, data_var, data_val, data_quest)
plt.savefig("participation.png", dpi = 250)
plt.show()
#%% Wohnungssuche
plot.plot_hist(12, data_var, data_val, data_quest, [1,2,3,4])
plt.savefig("looking_for_flat.png", dpi = 250)
plt.show()
#%% Wohnsituation Vergleich
plot.plot_hist(24, data_var, data_val, data_quest, [1,2,3,4,5])
plt.savefig("comparisson.png", dpi = 250)
plt.show()
#%% Wohnung finden
plot.plot_hist(26, data_var, data_val, data_quest, [1,2,3,4,5,6,7])
plt.savefig("find_flat.png", dpi = 250)
plt.show()

#%%
data_val['left'] = data_val['NT17_01']/((data_val['NT06_01']-1)/100)- data_val['NT17_01']
data_val.loc[data_val['left'] == np.inf, 'left'] = np.nan
data_val.loc[data_val['left']  > 2000, 'left'] = np.nan
left_nominal = []
for i in range(len(status_val)):
    part_nominal = np.nanmean(functions.condition(data_val, "left", "NT01", i+1, True))
    print(status_val[i])
    print(functions.condition(data_val, "left", "NT01", i+1, True))
    left_nominal.append(part_nominal)
    

y_pos = np.arange(len(status_val))

plt.barh(y_pos, left_nominal, align='center', alpha=0.7, edgecolor='black')
plt.yticks(y_pos, status_val)
plt.xlabel('Monatsbudget in €')
plt.title('Monatsbudget nach Abzug der Miete')
plt.tick_params(
    axis='y',
    which='both',  # major und minor ticks
    left=False     # ticks auf der y-Achse (links)
)

ax = plt.gca()
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# Annotate each bar with values from means_nominalplt.savefig("cost.png", dpi = 250)
plt.savefig("budget_after_rent.png", dpi = 250)
plt.show()

#%%


support_val = functions.condition(data_var, "MEANING", "VAR", "NT03")


left_nominal = []
for i in range(len(support_val)):
    part_nominal = np.nanmean(functions.condition(data_val, "left", "NT03", i+1, True)-1)
    left_nominal.append(part_nominal)
    

y_pos = np.arange(len(support_val))

plt.barh(y_pos, left_nominal, align='center', alpha=0.7, edgecolor='black')
plt.yticks(y_pos, support_val)
plt.xlabel('Monatsbudget in €')
plt.title('Monatsbudget nach Abzug der Miete')
plt.tick_params(
    axis='y',
    which='both',  # major und minor ticks
    left=False     # ticks auf der y-Achse (links)
)

ax = plt.gca()
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.savefig("budget_after_rent_2.png", dpi = 250)
# Annotate each bar with values from means_nominalplt.savefig("cost.png", dpi = 250)
plt.show()
#%%

data_val.loc[data_val['left'] > 1000, 'left'] = 1001

plt.figure(figsize=(8, 6))
bins = np.arange(0, 1101, 100)


# Calculate percentages for each bin
counts, bins = np.histogram(data_val['left'].dropna(), bins=bins)
total_counts = np.sum(counts)
percentages = [(counter / total_counts) * 100 for counter in counts]
plt.bar(bins[:-1], percentages, width=np.diff(bins), align='edge', alpha=0.7, edgecolor='black')
plt.vlines(502, 0, 35, color = "red")# Plot histogram with percentage labels on y-axis
plt.xticks(np.arange(0, 1001, 100))
plt.text(1101, -0.72, 'über 1000', ha='center', va='center')
plt.text(490, 9, 'Existenzminimum',rotation = "90",  ha='center', va='center', color = "red")
plt.xlabel('Monatsbudget nach Abzug der Warmmiete in €')
plt.ylabel('Anteil in %')
plt.title('Monatsbudget nach Abzug der Warmmiete')
plt.ylim(0,18)
# Show plot
plt.tight_layout()


limit = 502

# Filter 'left' column for values under the limit
values_under_limit = data_val['left'].dropna()[data_val['left'].dropna() < limit]

# Calculate the percentage
percentage_under_limit = (len(values_under_limit) / len(data_val['left'].dropna())) * 100

plt.title(f"{percentage_under_limit:.0f}% der Studierenden liegen nach Abzug der Warmmiete unter dem Existenzminimum")

plt.savefig("budget_after_rent_3.png", dpi = 250)
plt.show()

#%% Mietpreis
miete_durchschnitt = np.mean(data_val['NT17_01'].dropna())

#%% save text to txt
# with open('entries.txt', 'w') as file:
#     for index, row in data_val.iterrows():
#         file.write(f'Entry {index + 1}:\n')  # Write entry number
#         for item in row['NT11_01']:
#             file.write(f'- {item}\n')  # Write each item in the list with a bullet point
#         file.write('\n')  # Add a blank line between entries

# print("Entries saved to 'entries.txt'.")