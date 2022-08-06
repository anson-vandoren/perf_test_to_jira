import csv
import os
import sys

def main(csv_filename):
    with open(csv_filename, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        # read in the header row
        header_row = next(csv_reader)
        # read in the data row to a dictionary
        vals = next(csv_reader)

        to_delete = [x for x in range(0, 7)]
        for idx, item in enumerate(header_row):
          if item.lower().startswith('min'):
            to_delete.append(header_row.index(item))
          # replace underscores with spaces anywhere in the header
          header_row[idx] = item.replace('_', ' ')
          # replace PERC90 with P90
          header_row[idx] = header_row[idx].replace('PERC90', 'P90')
          # replace MEDIAN with MED
          header_row[idx] = header_row[idx].replace('MEDIAN', 'MED')

        # delete the items from both lists
        print(to_delete)
        print(header_row)

        header_row = [x for idx, x in enumerate(header_row) if idx not in to_delete]
        vals = [x for idx, x in enumerate(vals) if idx not in to_delete]
        print(header_row)

        for i in range(len(vals)):
            # if the value can be converted to a float, then convert it to a float
            try:
                vals[i] = float(vals[i])
            except ValueError:
                # otherwise, leave it as a string
                pass
            if isinstance(vals[i], float):
                vals[i] = int(round(vals[i], 0))
                # convert the value to a string with comma separators
                vals[i] = f"{vals[i]:,}"


        # make folder './output' if it doesn't exist
        if not os.path.exists('./output'):
            os.makedirs('./output')
        
        # write the data to a csv file
        with open(f'./output/{csv_filename}', 'w') as output_file:
            csv_writer = csv.writer(output_file)
            csv_writer.writerow(header_row)
            csv_writer.writerow(vals)
        
        # print the data to the terminal
        print(','.join(header_row))
        print(','.join(vals))
        print()
        print(format_as_markdown(header_row, vals))

def format_as_markdown(header_row, vals):
    # throughput headers are all headers where the second word is EPS or BPS
    throughput_headers = [x for x in header_row if x.split()[1].lower() in ['eps', 'bps']]
    throughput_indices = [header_row.index(x) for x in throughput_headers]
    # throughput values are all vals where index is in throughput_indices
    throughput_values = [vals[x] for x in throughput_indices]

    # usage headers are all headers that are not in throughput_headers
    usage_headers = [x for x in header_row if x not in throughput_headers]
    usage_indices = [header_row.index(x) for x in usage_headers]
    # usage values are all vals where index is in performance_indices
    usage_values = [vals[x] for x in usage_indices]

    # remove header and value anywhere where value is empty
    usage_headers = [x for i, x in enumerate(usage_headers) if usage_values[i] != '']
    usage_values = [x for i, x in enumerate(usage_values) if usage_values[i] != '']

    # remove header and value if header is MEM USAGE
    mem_usage_idx = header_row.index('MEM USAGE')
    usage_headers.remove('MEM USAGE')
    usage_values.remove(vals[mem_usage_idx])

    # construct two markdown tables
    tt_headers = ''
    tt_sep = ''
    tt_values = ''
    for i in range(len(throughput_headers)):
        longest = max(len(throughput_headers[i]), len(throughput_values[i]))
        tt_headers += f'|{throughput_headers[i].rjust(longest)}'
        tt_sep += f'|{"-" * longest}'
        tt_values += f'|{throughput_values[i].rjust(longest)}'
    throughput_table = f'{tt_headers}|\n{tt_sep}|\n{tt_values}|'

    ut_headers = ''
    ut_sep = ''
    ut_values = ''
    for i in range(len(usage_headers)):
        longest = max(len(usage_headers[i]), len(usage_values[i]))
        ut_headers += f'|{usage_headers[i].rjust(longest)}'
        ut_sep += f'|{"-" * longest}'
        ut_values += f'|{usage_values[i].rjust(longest)}'
    usage_table = f'{ut_headers}|\n{ut_sep}|\n{ut_values}|'
    return throughput_table + '\n\n' + usage_table


if __name__ == '__main__':
  # get first argument and pass to main() if it's a csv file
  if len(sys.argv) > 1 and sys.argv[1].endswith('.csv'):
    main(sys.argv[1])
  else:
    print('Usage: python main.py <csv_file>')
