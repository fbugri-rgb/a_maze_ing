#!/bin/bash

# ============================================================================
# A-MAZE-ING COMPREHENSIVE TEST SUITE
# Tests all functionality and edge cases
# ============================================================================

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Counters
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

PYTHON="/bin/python3"
MAIN="a_maze_ing.py"

# Print header
print_header() {
    echo -e "\n${CYAN}${BOLD}========================================${NC}"
    echo -e "${CYAN}${BOLD}$1${NC}"
    echo -e "${CYAN}${BOLD}========================================${NC}\n"
}

# Run a test
run_test() {
    local test_name=$1
    local command=$2
    
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    
    if eval "$command" > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} $test_name"
        PASSED_TESTS=$((PASSED_TESTS + 1))
        return 0
    else
        echo -e "${RED}✗${NC} $test_name"
        FAILED_TESTS=$((FAILED_TESTS + 1))
        return 1
    fi
}

print_header "A-MAZE-ING COMPREHENSIVE TEST SUITE"

# ============================================================================
# 1. CODE QUALITY TESTS
# ============================================================================
echo -e "${BOLD}1. CODE QUALITY TESTS${NC}"

run_test "Flake8 linting" "$PYTHON -m flake8 ."
run_test "Mypy type checking" "$PYTHON -m mypy --warn-return-any --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs ."

# ============================================================================
# 2. UNIT TESTS
# ============================================================================
echo -e "\n${BOLD}2. UNIT TESTS${NC}"

run_test "Module unit tests" "$PYTHON -m mazegen.tests.test_mazegen"

# ============================================================================
# 3. CONFIGURATION TESTS
# ============================================================================
echo -e "\n${BOLD}3. CONFIGURATION PARSING TESTS${NC}"

# Test valid configuration
cat > test_config_valid.txt << 'EOF'
WIDTH=10
HEIGHT=10
ENTRY=0,0
EXIT=9,9
OUTPUT_FILE=test_output.txt
PERFECT=True
EOF

run_test "Valid configuration" "$PYTHON $MAIN test_config_valid.txt"

# Test with comments
cat > test_config_comments.txt << 'EOF'
# This is a comment
WIDTH=10
HEIGHT=10  # inline comment
ENTRY=0,0
EXIT=9,9
OUTPUT_FILE=test_output2.txt
PERFECT=True
EOF

run_test "Configuration with comments" "$PYTHON $MAIN test_config_comments.txt"

# ============================================================================
# 4. MAZE GENERATION TESTS
# ============================================================================
echo -e "\n${BOLD}4. MAZE GENERATION TESTS${NC}"

# Perfect maze
cat > test_perfect.txt << 'EOF'
WIDTH=15
HEIGHT=12
ENTRY=0,0
EXIT=14,11
OUTPUT_FILE=test_perfect_maze.txt
PERFECT=True
EOF

run_test "Perfect maze generation (15×12)" "$PYTHON $MAIN test_perfect.txt"

# Imperfect maze
cat > test_imperfect.txt << 'EOF'
WIDTH=15
HEIGHT=12
ENTRY=0,0
EXIT=14,11
OUTPUT_FILE=test_imperfect_maze.txt
PERFECT=False
EOF

run_test "Imperfect maze generation (15×12)" "$PYTHON $MAIN test_imperfect.txt"

# Small maze
cat > test_small.txt << 'EOF'
WIDTH=5
HEIGHT=5
ENTRY=0,0
EXIT=4,4
OUTPUT_FILE=test_small_maze.txt
PERFECT=True
EOF

run_test "Small maze generation (5×5)" "$PYTHON $MAIN test_small.txt"

# Large maze
cat > test_large.txt << 'EOF'
WIDTH=30
HEIGHT=25
ENTRY=0,0
EXIT=29,24
OUTPUT_FILE=test_large_maze.txt
PERFECT=True
EOF

run_test "Large maze generation (30×25)" "$PYTHON $MAIN test_large.txt"

# ============================================================================
# 5. OUTPUT VALIDATION TESTS
# ============================================================================
echo -e "\n${BOLD}5. OUTPUT FILE VALIDATION${NC}"

# Check if output files exist
run_test "Perfect maze output exists" "test -f test_perfect_maze.txt"
run_test "Imperfect maze output exists" "test -f test_imperfect_maze.txt"
run_test "Small maze output exists" "test -f test_small_maze.txt"
run_test "Large maze output exists" "test -f test_large_maze.txt"

# Check if output files have content
run_test "Perfect maze has content" "test -s test_perfect_maze.txt"
run_test "Imperfect maze has content" "test -s test_imperfect_maze.txt"

# Validate hex format (should only contain valid hex characters and newlines)
run_test "Output contains valid hex characters" "grep -q '^[0-9A-F]*$' test_perfect_maze.txt"

# ============================================================================
# 6. EDGE CASES
# ============================================================================
echo -e "\n${BOLD}6. EDGE CASE TESTS${NC}"

# Entry and exit at same position (should still work)
cat > test_same_pos.txt << 'EOF'
WIDTH=10
HEIGHT=10
ENTRY=5,5
EXIT=5,5
OUTPUT_FILE=test_same_pos.txt
PERFECT=True
EOF

run_test "Entry equals exit" "$PYTHON $MAIN test_same_pos.txt"

# Different entry/exit positions
cat > test_diff_corners.txt << 'EOF'
WIDTH=10
HEIGHT=10
ENTRY=9,0
EXIT=0,9
OUTPUT_FILE=test_diff_corners.txt
PERFECT=True
EOF

run_test "Entry top-right, exit bottom-left" "$PYTHON $MAIN test_diff_corners.txt"

# ============================================================================
# SUMMARY
# ============================================================================

print_header "TEST SUMMARY"

echo -e "${BOLD}Total Tests:${NC}  $TOTAL_TESTS"
echo -e "${GREEN}${BOLD}Passed:${NC}       $PASSED_TESTS"
echo -e "${RED}${BOLD}Failed:${NC}       $FAILED_TESTS"

# Cleanup test files
echo -e "\n${BOLD}Cleaning up test files...${NC}"
rm -f test_*.txt

if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "\n${GREEN}${BOLD}🎉 ALL TESTS PASSED! 🎉${NC}\n"
    exit 0
else
    echo -e "\n${RED}${BOLD}❌ SOME TESTS FAILED ❌${NC}\n"
    exit 1
fi
