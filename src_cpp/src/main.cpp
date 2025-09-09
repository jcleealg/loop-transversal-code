#include <iostream>
#include <vector>
#include <string>
#include <stdexcept>
#include <fstream>
#include <sstream>
#include <limits>
#include "greedy_syndrome_mapper.hpp"

// Forward declarations
void print_vector(const std::vector<int>& vec);
void runMapper(const std::vector<std::vector<int>>& patterns);
void runExamples();
void processManualInput();
void processFileInput();
std::vector<std::vector<int>> load_patterns_from_file(const std::string& filepath);

void displayMenu() {
    std::cout << "\n---------- Greedy Syndrome Mapper CLI ----------\n";
    std::cout << "1. Run built-in examples\n";
    std::cout << "2. Enter error patterns manually\n";
    // TODO: Restore file loading functionality
    // std::cout << "3. Load error patterns from a file\n";
    std::cout << "4. Exit\n";
    std::cout << "--------------------------------------------\n";
    std::cout << "Please enter your choice: ";
}

int main() {
    // Run examples on startup
    runExamples();

    int choice = 0;
    while (true) {
        displayMenu();
        std::cin >> choice;

        if (std::cin.fail()) {
            std::cin.clear();
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
            std::cout << "\n[Error] Invalid input. Please enter a number.\n";
            continue;
        }
        
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');

        switch (choice) {
            case 1:
                runExamples();
                break;
            case 2:
                processManualInput();
                break;
            // TODO: Restore file loading functionality
            case 3:
                // processFileInput();
                std::cout << "\n[Info] File loading is temporarily disabled.\n";
                break;
            case 4:
                std::cout << "Exiting.\n";
                return 0;
            default:
                std::cout << "\n[Error] Invalid choice. Please try again.\n";
                break;
        }
    }
    return 0;
}

void print_vector(const std::vector<int>& vec) {
    std::cout << "[";
    for (size_t i = 0; i < vec.size(); ++i) {
        std::cout << vec[i] << (i == vec.size() - 1 ? "" : ", ");
    }
    std::cout << "]";
}

void runMapper(const std::vector<std::vector<int>>& patterns) {
    if (patterns.empty()) {
        std::cout << "No patterns to process.\n";
        return;
    }

    std::cout << "\nProcessing patterns...\n";
    try {
        GreedySyndromeMapper mapper(patterns);

        std::cout << "\nBasis mapping:" << std::endl;
        auto basis_map = mapper.get_basis_map_list();
        for (const auto& pair : basis_map) {
            std::cout << "  ";
            print_vector(pair.first);
            std::cout << " -> ";
            print_vector(pair.second);
            std::cout << std::endl;
        }

        std::cout << "\nParity Check Matrix:" << std::endl;
        Eigen::MatrixXi h_matrix = mapper.get_parity_check_matrix();
        if (h_matrix.size() == 0) {
            std::cout << "(empty matrix)" << std::endl;
        } else {
            std::cout << h_matrix << std::endl;
        }
    } catch (const std::exception& e) {
        std::cerr << "An error occurred: " << e.what() << std::endl;
    }
}

void runExamples() {
    std::cout << "\n=============== Running Examples ===============\n";
    
    std::cout << "\n--- Example 1: 7-dimensional basis vectors ---\n";
    std::vector<std::vector<int>> example1 = {
        {1,0,0,0,0,0,0}, {0,1,0,0,0,0,0}, {0,0,1,0,0,0,0}, 
        {0,0,0,1,0,0,0}, {0,0,0,0,1,0,0}, {0,0,0,0,0,1,0}, 
        {0,0,0,0,0,0,1}
    };
    std::cout << "Input patterns:" << std::endl;
    for(const auto& p : example1) { std::cout << "  "; print_vector(p); std::cout << std::endl; }
    runMapper(example1);

    std::cout << "\n--- Example 2: Patterns of burst error ---\n";
    std::vector<std::vector<int>> example2 = {
        {0,0,0,0,0,1}, {0,0,0,0,1,0}, {0,0,0,0,1,1}, {0,0,0,1,0,0}, 
        {0,0,0,1,1,0}, {0,0,1,0,0,0}, {0,0,1,1,0,0}, {0,1,0,0,0,0}, 
        {0,1,1,0,0,0}, {1,0,0,0,0,0}, {1,1,0,0,0,0}
    };
    std::cout << "Input patterns:" << std::endl;
    for(const auto& p : example2) { std::cout << "  "; print_vector(p); std::cout << std::endl; }
    runMapper(example2);
    
    std::cout << "\n============= Examples Finished ==============\n";
}

void processManualInput() {
    std::cout << "\nEnter all error patterns on a single line.\n";
    std::cout << "Use commas (,) to separate patterns and spaces for numbers within a pattern.\n";
    std::cout << "Example: 1 0 0, 0 1 0, 1 1 0\n";
    std::cout << "> ";

    std::string line;
    if (!std::getline(std::cin, line) || line.empty()) {
        std::cout << "No input provided.\n";
        return;
    }

    std::vector<std::vector<int>> patterns;
    std::stringstream line_stream(line);
    std::string pattern_str;

    // Split the line by commas to get individual patterns
    while (std::getline(line_stream, pattern_str, ',')) {
        std::vector<int> pattern;
        std::stringstream pattern_stream(pattern_str);
        int val;

        // Split the pattern string by spaces to get numbers
        while (pattern_stream >> val) {
            pattern.push_back(val);
        }

        if (!pattern.empty()) {
            patterns.push_back(pattern);
        }
    }

    runMapper(patterns);
}

std::vector<std::vector<int>> load_patterns_from_file(const std::string& filepath) {
    std::ifstream file(filepath);
    if (!file.is_open()) {
        throw std::runtime_error("Could not open file: " + filepath);
    }

    std::vector<std::vector<int>> patterns;
    std::string line;
    while (std::getline(file, line)) {
        // Ignore comments and empty lines
        if (line.empty() || line[0] == '#') {
            continue;
        }
        std::vector<int> pattern;
        std::stringstream ss(line);
        int val;
        while (ss >> val) {
            pattern.push_back(val);
            if (ss.peek() == ',' || ss.peek() == ' ') {
                ss.ignore();
            }
        }
        if (!pattern.empty()) {
            patterns.push_back(pattern);
        }
    }
    return patterns;
}

void processFileInput() {
    std::cout << "Enter the path to the file: ";
    std::string filepath;
    std::getline(std::cin, filepath);
    
    // Trim whitespace from filepath, e.g., from pressing enter on an empty line
    size_t first = filepath.find_first_not_of(" \t\n\r");
    if (std::string::npos == first) {
        std::cout << "No filepath entered.\n";
        return;
    }
    size_t last = filepath.find_last_not_of(" \t\n\r");
    filepath = filepath.substr(first, (last - first + 1));

    try {
        auto patterns = load_patterns_from_file(filepath);
        runMapper(patterns);
    } catch (const std::exception& e) {
        std::cerr << "\n[Error] " << e.what() << std::endl;
    }
}