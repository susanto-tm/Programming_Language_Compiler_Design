func hashtags(let i, let j) {
    if i <= 0 or i > j{
        return;
    }

    print(i * "#");
    hashtags(i + 1, j);
    print(i * "#");
}
hashtags(3, 9);