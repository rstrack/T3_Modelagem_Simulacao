class GNPCL():
    """
    Gerador de números pseudo-aletórios congruencial linear.
 

    Atributos:
    ----------
    seed : int
        número inicial do gerador
    exp : int
        expoente para geração do módulo
    mod : int
        módulo utilizado para congruência. Preferencialmente o maior inteiro possível
    c : int   
        constante de incremento (padrão: 0)

    Métodos:
    ----------
    new_seed(seed: int)
        define nova seed para o gerador, iniciando um novo ciclo de geração
    generate() -> float
        gera o próximo número do gerador
    """
    exp = 61
    mod = 2**exp - 1
    # a = mod**(0.5)
    # a = float(2**(EXP/2))
    t = 7777777
    a = 8*t+3
    # a = float(8*T-3)
    c = 2**17 - 1 # primo de mersenne

    def __init__(self, seed: int) -> None:
        self.prev = seed

    def new_seed(self, seed: int) -> None:
        self.prev = seed

    def generate(self) -> float:
        self.prev = (self.a * self.prev + self.c) % self.mod
        return self.prev/self.mod
