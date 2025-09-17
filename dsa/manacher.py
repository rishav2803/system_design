class Manacher:
    def __init__(self, s: str):
        self.s_prime = "#" + "#".join(s) + "#"
        self.n = len(self.s_prime)
        self.palindrome_radii = self._build()

    def _build(self, center: int = 0, right_boundary: int = 0):
        palindrome_radii = [0] * self.n

        for i in range(self.n):
            if i < right_boundary:
                mirror_idx = 2 * center - i
                palindrome_radii[i] = min(
                    # because till right we know a correct palindrome exist so we try to keep
                    # the intial palindrome_radii to be inside right in case it overflows
                    right_boundary - i,
                    # this will give the val of the mirr of the curr idx if this overflows we take right - i
                    palindrome_radii[mirror_idx],
                )

            # now we have starting point we try to expand from the curr palindrom_radii
            # if palindrome[i] is 2 it means that we knwo 2 forward and backard palindrome
            # that is why we do i + palindrome[i] + 1 we skip those 2 and start from after that

            # iterate till left rightmatch and we are inside the boundary
            while (
                i + palindrome_radii[i] + 1 < self.n
                and i - palindrome_radii[i] - 1 >= 0
                and self.s_prime[i + palindrome_radii[i] + 1]
                == self.s_prime[i - palindrome_radii[i] - 1]
            ):
                palindrome_radii[i] += 1

            # Update center and right boundary if this palindrome expands beyond it
            if i + palindrome_radii[i] > right_boundary:
                center = i
                right_boundary = i + palindrome_radii[i]

        return palindrome_radii

    def count_palindromic_substrings(self) -> int:
        return sum((r + 1) // 2 for r in self.palindrome_radii)


if __name__ == "__main__":
    s = "abba"
    manacher = Manacher(s)
    print("Manacher arr is", manacher.palindrome_radii)
