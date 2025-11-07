import csv
from datetime import datetime, timedelta

class OrcamentoAluguel:
    def __init__(self):
        self.valores_base = {"apartamento": 700, "casa": 900, "estudio": 1200}
        self.valor_contrato = 2000
        self.max_parcelas = 5
    
    def calcular(self, tipo, quartos=1, garagem=0, tem_criancas=True):
        valor = self.valores_base[tipo.lower()]
        if tipo.lower() == "apartamento" and quartos == 2:
            valor += 200
        elif tipo.lower() == "casa" and quartos == 2:
            valor += 250
        if tipo.lower() in ["apartamento", "casa"]:
            valor += garagem * 300
        elif tipo.lower() == "estudio":
            if garagem <= 2:
                valor += 250
            else:
                valor += 250 + (garagem - 2) * 60
        if tipo.lower() == "apartamento" and not tem_criancas:
            valor *= 0.95
        return round(valor, 2)
    
    def gerar_csv(self, valor_mensal, nome_arquivo="orcamento.csv"):
        parcelas = []
        data_base = datetime.now()
        for i in range(12):
            data_vencimento = data_base + timedelta(days=30 * (i + 1))
            parcelas.append([f"Parcela {i+1}", data_vencimento.strftime("%d/%m/%Y"), f"R$ {valor_mensal:.2f}"])
        with open(nome_arquivo, 'w', newline='', encoding='utf-8') as arquivo:
            writer = csv.writer(arquivo)
            writer.writerow(["Parcela", "Vencimento", "Valor"])
            writer.writerows(parcelas)
        return nome_arquivo

def main():
    orcamento = OrcamentoAluguel()
    print("=== ORÇAMENTO DE ALUGUEL - R.M IMOBILIÁRIA ===\n")
    tipo = input("Tipo (apartamento/casa/estudio): ").strip().lower()
    quartos = int(input("Quantidade de quartos (1 ou 2): "))
    garagem = int(input("Quantidade de vagas: "))
    tem_criancas = input("Possui crianças? (s/n): ").strip().lower() == 's'
    valor_mensal = orcamento.calcular(tipo, quartos, garagem, tem_criancas)
    print(f"\nValor do aluguel mensal: R$ {valor_mensal:.2f}")
    print(f"Valor do contrato: R$ {orcamento.valor_contrato:.2f}")
    parcelas_contrato = int(input(f"Em quantas vezes deseja parcelar o contrato? (1 a {orcamento.max_parcelas}): "))
    while parcelas_contrato < 1 or parcelas_contrato > orcamento.max_parcelas:
        parcelas_contrato = int(input(f"Por favor, informe um valor entre 1 e {orcamento.max_parcelas}: "))
    valor_parcela_contrato = orcamento.valor_contrato / parcelas_contrato
    print(f"Valor da parcela do contrato ({parcelas_contrato}x): R$ {valor_parcela_contrato:.2f}")
    nome_csv = orcamento.gerar_csv(valor_mensal)
    print(f"Arquivo CSV gerado: {nome_csv}")

if __name__ == "__main__":
    main()

