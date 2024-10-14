import argparse
import re
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def extract_SPRTA_scores(input_file_path):
	# Read the content of the text file
	with open(input_file_path, 'r') as file:
		input_string = file.read()

	# replace None by 999.0
	input_string = input_string.replace("None","999.0")

	# Regular expression pattern to find all pairs of support and IQsupport values
	pattern = r'sprta=(\d+\.\d+).*?input_sprta=(\d+\.\d+)'

	# Find all matches in the input string
	matches = re.findall(pattern, input_string)

	# Initialize arrays to store MAPLE and CMAPLE scores
	MAPLE_scores = []
	CMAPLE_scores = []

	# Process and store each pair of values in the respective arrays
	for match in matches:
		MAPLE_score, CMAPLE_score = match
		MAPLE_scores.append(float(MAPLE_score))
		CMAPLE_scores.append(float(CMAPLE_score))
	
	return MAPLE_scores, CMAPLE_scores


def plot_SPRTA_scores(MAPLE_scores, CMAPLE_scores, output_file_path):

	# Draw a scatter plot
	plt.scatter(MAPLE_scores, CMAPLE_scores, color='red', marker='o')
	# draw a diagonal line
	plt.plot([0, 1], [0, 1], color='blue', linestyle='-', linewidth=2)
	# Labeling the axes
	plt.xlabel('Latest CMAPLE')
	plt.ylabel('CMAPLE baseline')
	# Set the range for the axes (0 to 1 for both axes)
	plt.xlim(0, 1)
	plt.ylim(0, 1)
	# Title of the plot
	plt.title('Scatter Plot of SPRTA computed by the two versions of CMAPLE')
	# Save the plot to the output file
	plt.savefig(output_file_path + ".png")
	# Optional: Clear the current plot if you plan to create another plot
	plt.clf()

	# Write SPRTA computed by MAPLE and CMAPLE to a file
	with open(output_file_path + ".txt", 'w') as data_file:
		data_file.write("Latest_CMAPLE,CMAPLE_baseline,30_percent_diff\n")
		for MAPLE_score, CMAPLE_score in zip(MAPLE_scores, CMAPLE_scores):
			if (CMAPLE_score) <= 1 and (abs(MAPLE_score - CMAPLE_score) >= 0.3):
				data_file.write(f"{MAPLE_score},{CMAPLE_score},YES\n")
			else:
				data_file.write(f"{MAPLE_score},{CMAPLE_score}, \n")

	print(f"Scatter plot saved to {output_file_path}.png and {output_file_path}.txt")

def main():
	# input params
	parser = argparse.ArgumentParser(description='Extract and visualize SPRTA scores computed by the two versions of CMAPLE.')
	parser.add_argument('--input', default="", help='The treefile with SPRTA scores')
	parser.add_argument('--output', default="", help='The output file path')

	# parse params
	args = parser.parse_args()
	input_path = args.input
	output_path = args.output

	# extract SPRTA scores
	MAPLE_scores, CMAPLE_scores = extract_SPRTA_scores(input_path)

	# visualize the results
	plot_SPRTA_scores(MAPLE_scores, CMAPLE_scores, output_path)

# Call the main function
if __name__ == "__main__":
	main()















