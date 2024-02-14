import streamlit as st
import yaml

def get_matrix_input(n, m):
    input_matrix = st.text_input(f"Enter the 2D matrix of shape {n}x{m} values separated by comma, columns seperated by |", key=f"input_matrix_{n}_{m}")
    if input_matrix != "":
        input_matrix = input_matrix.split('|')
        input_matrix = [i.split(',') for i in input_matrix]
        input_matrix = [[float(j) for j in i] for i in input_matrix]

        if len(input_matrix) != n or len(input_matrix[0]) != m:
            st.error(f"Shape of input matrix should be {n}x{m}")
        else:
            return input_matrix

def main():
    st.title("Data Generator - Graph Based - Config Generator")

    super_nodes_data = {}

    super_nodes_data['n_supernodes'] = st.number_input("Enter number of super nodes", 1, step=1)

    super_nodes_data['n_cycles'] = st.number_input("Enter number of cycles", 100, step=100)

    super_nodes_data['supernodes'] = {}
 

    for i in range(super_nodes_data['n_supernodes']):

        st.subheader(f"Super Node {i+1}")

        n_nodes = st.number_input(f"Enter number of sub nodes for Super Node {i+1}", 1, step=1)

        control_points = []

        control_points_in = st.text_input(f"Enter comma separated control points for Super Node {i+1}")

        if control_points_in:
            control_points = [float(x) for x in control_points_in.split(',')]

        node_type = st.selectbox(f"Select type for Super Node {i+1}", ['independent', 'dependent'])

        
        if node_type == 'dependent':
            n_incoming_nodes = st.number_input(f"Enter number of incoming nodes for Super Node {i+1}", 1, step=1)

            inputs = []

            for j in range(n_incoming_nodes):
                
                st.subheader(f"Incomming Node {j+1} for Super Node {i+1}")

                input_supernode = st.selectbox(f"Incomming Node {j+1} for Super Node {i+1}", list(super_nodes_data['supernodes'].keys()))

                if input_supernode is not None:
                    correlation = st.number_input(f"Correlation for Incomming Node {j+1} for Super Node {i+1}", -1.0, 1.0, 0.0)
                    weight = st.number_input(f"Weight for Incomming Node {j+1} for Super Node {i+1}", 0.0, 1.0, 0.0)
                    
                    connections_main = []
                    for k in range(n_nodes):
                        connection = st.text_input(f"Enter comma separated connections for Sub Node {k+1}")

                        connections = list(int(x) for x in connection.split(',')) if connection else []

                        connections_main.append(connections)

                    expected_lower_bound = st.number_input(f"Enter expected lower bound for Incomming node {j+1} for Super Node {i+1}")
                    expected_upper_bound = st.number_input(f"Enter expected upper bound for Incomming node {j+1} for Super Node {i+1}")
                    expected_mean = st.number_input(f"Enter expected mean for Incomming node {j+1} for Super Node {i+1}")

                    inputs.append({
                        'input_supernode': input_supernode,
                        'correlation': correlation,
                        'weight': weight,
                        'connections': connections,
                        'expected_lower_bound': expected_lower_bound,
                        'expected_upper_bound': expected_upper_bound,
                        'expected_mean': expected_mean
                    })
        else:
            n_incoming_nodes = 0
            inputs = []
        
        boundaries = []
        for j in range(n_nodes):
            bounds = st.text_input(f"Enter comma separated bounds for Sub Node {j+1} for Super Node {i+1}")

            if bounds:
                bounds = [float(x) for x in bounds.split(',')]
            else:
                bounds = [0,1]

            boundaries.append(bounds)

        super_nodes_data['supernodes'][i] = {
            'node_type': node_type,
            'n_subnodes': n_nodes,
            'boundaries': boundaries,
            'control_points': control_points,
            'n_incomming_nodes': n_incoming_nodes,
            'inputs': inputs
        }




    # Convert the dictionary into a YAML formatted string
    yaml_config = yaml.dump(super_nodes_data)

    # Create a download button for the YAML configuration file
    st.download_button(
        label="Download YAML Configuration File",
        data=yaml_config,
        file_name='config.yaml',
        mime='application/x-yaml'
    )

if __name__ == "__main__":
    main()