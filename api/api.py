from flask import Flask, request
import subprocess
import pandas as pd
from mockresults import *

app = Flask(__name__)

@app.route('/annotate', methods=['POST'])
def annotate_vcf():
    # Get the input file path from the request
    #input_path = request.form['input']

    # Set the output file path
    #output_path = 'output.vcf'

    # Define the command to run the Snakemake pipeline
    #cmd = f'snakemake --config input_file={input_path} output_file={output_path}'
    cmd = f'snakemake --cores 1 results/annotated_variants.vcf'    

    # Run the command
    subprocess.run(cmd, shell=True)

    # Return a success message
    return 'Annotation complete.'

#@app.route('/filter')
#def results():
    # get data and process it
    #TODO if file not exists
    # Make a request to the API endpoint and retrieve the output vcf file
#    r = requests.get('http://localhost:5000/results/annotated.vcf')
    #vcf_content = r.text
    
    # Parse the contents of the output vcf file using pandas
    #vcf_df = pd.read_csv(vcf_content, sep='\t', comment='#', header=None)
    #vcf_json = vcf_df.to_json(orient='split')

    # render the template with processed data
    #return render_template('filter.html', table_data=vcf_json)

@app.route('/result')
def result():
    # Read the results from the output file
    vcf_results = pd.read_csv('/app/results/annotated_output.vcf', sep='\t', comment='#', header=None)
    
    # Convert the results to a list of lists
    rows = []
    for index, row in vcf_results.iterrows():
        annotation = row[7].split(';')[0]
        rows.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], annotation])
    
    return render_template('result.html', rows=rows)

if __name__ == '__main__':
    app.run(debug=True, port=5000)