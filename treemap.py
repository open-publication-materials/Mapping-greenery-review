import squarify
import matplotlib.pyplot as plt

# Reordered data from detailed to broad spatial scales
labels = ['Site', 'Road', 'Neighborhood', 'City', 'Region', 'Country', 'Mixed']
sizes = [17, 12, 26, 45, 21, 4, 22]  # Reordered sizes

# Calculate percentages for the labels and place them on a new line
total = sum(sizes)
labels_with_percentages_newline = [f'{label}\n({size/total*100:.1f}%)' for label, size in zip(labels, sizes)]

# Blue color palette for better contrast
colors = ['#d0e1f9', '#9ecae1', '#74a9cf', '#6baed6', '#2b8cbe', '#045a8d', '#023858']

# Create the treemap
plt.figure(figsize=(10, 6))
squarify.plot(sizes=sizes, label=labels_with_percentages_newline, color=colors, alpha=.8,
              text_kwargs={'fontsize': 12, 'color': 'white', 'weight': 'bold'})  # Set font size and color
plt.title("Scale of Analysis Treemap", fontsize=16, color='black')
plt.axis('off')  # Remove axes for better visual presentation

# Save the figure as a PNG file
plt.savefig('scale_of_analysis_treemap_reordered.png', dpi=300, bbox_inches='tight')

# Show the plot
plt.show()
