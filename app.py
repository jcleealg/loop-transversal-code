import streamlit as st
import ast
import pandas as pd
import numpy as np
from io import StringIO
import json

# Import from your existing project files
from greedy_syndrome_mapper import GreedySyndromeMapper
from main import load_patterns

st.set_page_config(layout="wide")

st.title("Greedy Syndrome Mapper")
st.write("An interactive web app for the Loop Transversal Code project.")

# --- Input Section ---
st.sidebar.header("Input Error Patterns (T)")

input_method = st.sidebar.radio(
    "Choose an input method:",
    ("Standard Basis", "Text Input", "Upload File")
)

patterns = None

if input_method == "Standard Basis":
    st.sidebar.subheader("Generate Standard Basis Vectors")
    n_basis = st.sidebar.number_input("Enter the dimension (n):", min_value=2, max_value=16, value=3, step=1)
    if n_basis:
        patterns = load_patterns(standard_basis=n_basis)

elif input_method == "Text Input":
    st.sidebar.subheader("Enter Patterns as a Python List")
    patterns_str = st.sidebar.text_area(
        "e.g., [[1, 0, 0], [0, 1, 0], [0, 0, 1]]",
        height=200
    )
    if patterns_str:
        try:
            patterns = ast.literal_eval(patterns_str)
        except (ValueError, SyntaxError) as e:
            st.error(f"Invalid Python literal format: {e}")
            patterns = None

elif input_method == "Upload File":
    st.sidebar.subheader("Upload a .txt file")
    uploaded_file = st.sidebar.file_uploader("Each line should be a vector, e.g., [1, 0, 0]", type=["txt"])
    if uploaded_file is not None:
        try:
            stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
            lines = stringio.readlines()
            patterns = [ast.literal_eval(line.strip()) for line in lines if line.strip()]
        except Exception as e:
            st.error(f"Error reading or parsing file: {e}")
            patterns = None

# --- Execution and Display Section ---
if st.button("▶️ Generate Mapping"):
    if patterns:
        # 上方：Input 概覽（raw style, 可換行，依頁面寬度自動換行）
        st.header("Input")
        st.subheader("Error Patterns — Raw View")

        try:
            # compact_json 為單行 JSON（使用最少空白），不含縮排
            compact_json = json.dumps(patterns, ensure_ascii=False, separators=(",", ":"))
        except Exception:
            compact_json = str(patterns)

        # 直接顯示 compact JSON（字串），讓介面根據頁面寬度換行
        st.subheader("Error Patterns (compact)")
        st.write(compact_json)

        # 下載 compact JSON
        try:
            st.download_button("Download patterns (JSON)", compact_json.encode('utf-8'), "patterns.json", "application/json")
        except Exception:
            pass

        st.markdown("---")

        # 下方：Results（由上到下顯示）
        st.header("Results")

        try:
            with st.spinner('Running the greedy algorithm...'):
                mapper = GreedySyndromeMapper(patterns)

            tab_full, tab_basis, tab_h = st.tabs(["Full Syndrome Mapping", "Basis Mapping", "Parity Check Matrix (H)"])

            with tab_full:
                st.subheader("Full Syndrome Mapping")
                full_map_data = [{"Vector": str(k), "Syndrome": str(v)} for k, v in sorted(mapper.syndrome_map.items())]
                if full_map_data:
                    df_full = pd.DataFrame(full_map_data)
                    st.dataframe(df_full, height=420, use_container_width=True)
                    try:
                        st.download_button("Download full mapping (CSV)", df_full.to_csv(index=False).encode('utf-8'), "full_mapping.csv", "text/csv")
                    except Exception:
                        pass
                else:
                    st.info("No full mapping available.")

            with tab_basis:
                st.subheader("Basis Mapping")
                basis_map_list = mapper.get_basis_map_list()
                basis_map_data = [{"Basis Vector": str(item[0]), "Syndrome": str(item[1])} for item in basis_map_list]
                if basis_map_data:
                    df_basis = pd.DataFrame(basis_map_data)
                    st.dataframe(df_basis, height=420, use_container_width=True)
                    try:
                        st.download_button("Download basis mapping (CSV)", df_basis.to_csv(index=False).encode('utf-8'), "basis_mapping.csv", "text/csv")
                    except Exception:
                        pass
                else:
                    st.info("No basis mapping available.")

            with tab_h:
                st.subheader("Parity Check Matrix (H)")
                parity_matrix = mapper.get_parity_check_matrix()
                try:
                    st.text("Matrix dimensions: " + str(parity_matrix.shape))
                    st.dataframe(pd.DataFrame(parity_matrix), height=420, use_container_width=True)
                    try:
                        st.download_button("Download parity matrix (CSV)", pd.DataFrame(parity_matrix).to_csv(index=False).encode('utf-8'), "parity_matrix.csv", "text/csv")
                    except Exception:
                        pass
                except Exception:
                    st.write(parity_matrix)

        except (ValueError, RuntimeError, IndexError) as e:
            st.error(f"An error occurred during mapping: {e}")
    else:
        st.warning("Please provide error patterns using one of the methods on the left.")

st.sidebar.info("After providing input, click the 'Generate Mapping' button to see the results.")
