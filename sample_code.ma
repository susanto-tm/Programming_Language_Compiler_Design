// Variable assignment
let var1 = 0;
let var2 = 20;
let var3;

// Conditional Statements
if var1 == 0 {
    print(var1);
}
else {
    if var2 - var3 == 0 {
        print(var3);
    }
    else {
        print(var2);
    }
}

// Loops and Functions

// Bubble Sort
func bubble_sort(let lst) {
    let n = len(lst);
    for i := range n {
        for j := range n-1-i {
            if lst[j] > lst[j+1] {
                let temp = lst[j];
                lst[j] = lst[j+1];
                lst[j+1] = temp;
            }
        }
    }
    return lst;
}

// Insertion Sort
func insertion_sort(let lst) {
    let n = len(lst);
    for i := range 1...n {
        let j = i;
        for j > 0 and lst[j] < lst[j-1] {
            let temp = lst[j];
            lst[j] = lst[j-1];
            lst[j-1] = temp;
            j--;
        }
    }
    return lst;
}

// Selection Sort
func selection_sort(let lst) {
    let n = len(lst);
    for i := range n {
        let min_idx = i;
        for j := range (i+1)...n {
            if lst[j] < lst[min_idx] {
                min_idx = j;
            }
        }
        let temp = lst[i];
        lst[i] = lst[min_idx];
        lst[min_idx] = temp;
    }
    return lst;
}

// Backtracking
func hashtags(let i, let j) {
    if i <= 0 or i > j {
        return;
    }

    print(i * "#");
    hashtags(i + 1, j);
    print(i * "#");

}

hashtags(1, 9);
print();

print(insertion_sort([1, 3, 2, 3, 10, 0, -1, -100]));
print();

// Lists

// List Generation
let arr = [0...20, 2];
print("All even numbers from 0 to 20:", arr);
print();

// List Indexing
let arr1 = [1, 2, [3, 4, [5, 6], 7], 8];
print("Element [5, 6] using indices by calling arr1[2, 2]:", arr1[2, 2]);

// List Slicing
print("Element [3, 4, [5, 6]] using slicing and indexing by calling arr1[2, 0:3]:", arr1[2, 0:3]);
print();

// Built-in Mathematical Functions and Inline Functions

// Integral

// Indefinite
f(x) = integrate("3*x^2 + 2*x + 4", "x");
print("Integral is:", integrate("3*x^2 + 2*x + 4", "x"));
print("At x = 5, f(x) is:", f(5));
print();

// Definite
print("Definite integral from 0 to 5 is:", integrate("3*x^2 + 2*x + 4", "x", 0, 5));
print();

// Differentiation
g(x) = diff("3*x^2 + 2*x + 4", "x");
print("Derivative of g(x) is:", diff("3*x^2 + 2*x + 4", "x"));
print("At x = 5, g(x) is:", g(5));
print();

// Trigonometric Functions

print("sin(30, 'deg'):", sin(30, 'deg'), ", cos(30, 'deg'):", cos(30, 'deg'), ", tan(30, 'deg'):", tan(30, 'deg'));
print("asin(4, 5):", asin(4, 5), ", acos(4, 5):", acos(4, 5), ", atan(4, 5):", atan(4, 5));
print("sinh(30, 'deg'):", sinh(30, 'deg'), ", cosh(30, 'deg'):", cosh(30, 'deg'), ", tanh(30, 'deg'):", tanh(30, 'deg'));
print();

// Minimum Maximum
print("Minimum in ([1, 3, 4, 100], [200, 180, 0], 1) is:", min([1, 3, 4, 100], [200, 180, 0], 1));
print("Maximum in ([1, 3, 4, 100], [200, 180, 0], 1) is:", max([1, 3, 4, 100], [200, 180, 0], 1));






