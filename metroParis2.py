# -*- coding: utf-8 -*-
"""
Created on Sun Apr 18 04:03:25 2021

@author: Guilherme Costa
"""

from queue import PriorityQueue
from copy import deepcopy

dist_reta = [[0,10,18.5,24.8,36.4,38.8,35.8,25.4,17.6,9.1,16.7,27.3,27.6,29.8],
[10 ,0 ,8.5 ,14.8 ,26.6 ,29.1 ,26.1 ,17.3 ,10 ,3.5 ,15.5 ,20.9 ,19.1 ,21.8],
[18.5, 8.5, 0, 6.3, 18.2, 20.6, 17.6, 13.6, 9.4, 10.3, 19.5, 19.1, 12.1, 16.6],
[24.8, 14.8, 6.3, 0, 12, 14.4, 11.5, 12.4, 12.6, 16.7, 23.6, 18.6, 10.6, 15.4],
[36.4, 26.6, 18.2, -1, 0, 3, 2.4, 19.4, 23.3, 28.2, 34.2, 24.8, 14.5, 17.9],
[38.8, 29.1, 20.6, 14.4, 3, 0, 3.3, 22.3, 25.7, 30.3, 36.7, 27.6, 15.2, 18.2],
[35.8, 26.1, 17.6, 11.5, 2.4, 3.3, 0, 20, 23, 27.3, 34.2, 25.7, 12.4, 15.6],
[25.4, 17.3, 13.6, 12.4, 19.4, 22.3, 20, 0, 8.2, 20.3, 16.1, 6.4, 22.7, 27.6],
[17.6, 10, 9.4, 12.6, 23.3, 25.7, 23, 8.2, 0, 13.5, 11.2, 10.9, 21.2, 26.6],
[9.1, 3.5, 10.3, 16.7, 28.2, 30.3, 27.3, 20.3, 13.5, 0, 17.6, 24.2, 18.7, 21.2],
[16.7, 15.5, 19.5, 23.6, 34.2, 36.7, 34.2, 16.1, 11.2, 17.6, 0, 14.2, 31.5, 35.5],
[27.3, 20.9, 19.1, 18.6, 24.8, 27.6, 25.7, 6.4, 10.9, 24.2, 14.2, 0, 28.8, 33.6],
[27.6, 19.1, 12.1, 10.6, 14.5, 15.2, 12.4, 22.7, 21.2, 18.7, 31.5, 28.8, 0, 5.1],
[29.8, 21.8, 16.6, 15.4, 17.9, 18.2, 15.6, 27.6, 26.6, 21.2, 35.5, 33.6, 5.1, 0]]

dist_real = [[0,10,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                  [10, 0, 8.5,-1,-1,-1,-1,-1,10,3.5,-1,-1,-1,-1],
                  [-1, 8.5,0,6.3,-1,-1,-1,-1,9.4,-1,-1,-1, 18.7,-1],
                  [-1,-1,6.3,0,13,-1,-1,15.3,-1,-1,-1,-1,12.8,-1],
                  [-1,-1,-1,13,0,3,2.4,30,-1,-1,-1,-1,-1,-1],
                  [-1,-1,-1,-1,3,0,-1,-1,-1,-1,-1,-1,-1,-1],
                  [-1,-1,-1,-1,2.4,-1,0,-1,-1,-1,-1,-1,-1,-1],
                  [-1,-1,-1,15.3,30,-1,-1,0,9.6,-1,-1,6.4,-1,-1],
                  [-1,10,9.4,-1,-1,-1,-1,9.6,0,-1,12.2,-1,-1,-1],
                  [-1,3.5,-1,-1,-1,-1,-1,-1,-1,0,-1,-1,-1,-1],
                  [-1,-1,-1,-1,-1,-1,-1,-1,12.2,-1,0,-1,-1,-1],
                  [-1,-1,-1,-1,-1,-1,-1,6.4,-1,-1,-1,0,-1,-1],
                  [-1,-1,18.7,12.8,-1,-1,-1,-1,-1,-1,-1,-1,0,5.1],
                  [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,5.1,0]]

##Variavel que guarda as estações que podem ser visitadas por cada nó ##
estacoes_filhas = [[2],#E1
           [1,3,9,10],#E2
           [2,4,9,13],#E3
           [3,5,8,13],#E4
           [4,6,7,8],#E5
           [5],#E6
           [5],#E7
           [4,5,9,12],#E8
           [2,3,8,11],#E9
           [2],#E10
           [9],#E11
           [8],#E12
           [3,4,14],#E13
           [13]]#E14

#lista que guarda a cor da linha
'''0 = azul
   1 = vermelho
   2 = amarelo
   3 = verde
   indice + 1= numero da estacao
   ex cor_estacao[0] é a cor da estacao E1'''
cor_estacao = [[0],[0,2],[0,1],[0,3],[0,2],[0],[2],[2,3],[2,1],[2],[1],[3],[1,3],[3]]

#Classe Estado - Guarda os valores do estado atual

class Estado(object):
    def __init__(self, valor, pai, velocidade, t_bald, linhaAtual, inicio = 0, destino = 0):
        self.filhos = []
        self.pai = pai
        self.valor = valor
        self.linhaAtual = linhaAtual
        self.t_bald = t_bald
        
        if pai:
            self.caminho = pai.caminho
            self.caminho.append(valor)
            self.inicio = pai.inicio
            self.destino = pai.destino
            self.velocidade = velocidade
        
        else: # Se não tiver pai, significa que é o estado inicial. adicionamos o valor ao caminho e defininmos o inicio e o destino
        
            self.caminho = [valor]
            self.inicio = inicio
            self.destino = destino
            self.velocidade = velocidade
    
    #funções implementadas na classe filha Estado_Atual
    def GetDistanciaReal(self):
        pass
    
    def GetTempoTotal(self):
        pass
        
    def GetDistanciaReta(self):
        pass
    
    def CriarFilhos(self):
        pass
    
    
class Estado_Atual(Estado): #herda da classe Estado
    
    def __init__(self, valor, pai, velocidade, t_bald, linhaAtual, inicio = 0, destino = 0):
        super(Estado_Atual, self).__init__(valor, pai, velocidade, t_bald, linhaAtual, inicio, destino)
        self.baldeacaoPresente = self.GetBaldeacaoPresente()
        self.baldeacaoFuturo = self.GetBaldeacaoFuturo()
        self.distanciaReal = self.GetDistanciaReal()
        self.distanciaReta = self.GetDistanciaReta()
        self.custo = self.GetCusto()
        self.tempo = self.GetTempoTotal()
        
    #retorna o custo da aresta
    def GetDistanciaReal(self):
        if self.pai == 0:
            return 0
        if (self.pai) != 0:
            self.distanciaReal = (dist_real[(self.pai).valor - 1][self.valor-1])*60/self.velocidade
        if self.baldeacaoPresente == True:
            self.distanciaReal += t_bald
        
        return self.distanciaReal
    
    def GetTempoTotal(self):
        if(self.valor == self.inicio):
            return 0
        return self.distanciaReal + (self.pai).tempo
        
    #Calcula o valor da heurística
    def GetDistanciaReta(self):
        if self.valor == self.destino:
            return 0
        self.distanciaReta = ((dist_reta[self.valor-1][self.destino-1])*60)/self.velocidade
        if self.baldeacaoFuturo == True:
            self.distanciaReta += t_bald
        return self.distanciaReta
    
    def GetCusto(self):
        if self.pai == 0 or self.velocidade == 0:
            return 0
        return (self.distanciaReal + self.distanciaReta) + (self.pai).distanciaReal
    
    def encontrarLinha(self,prox):
        cor = list(set(cor_estacao[self.valor - 1]).intersection(cor_estacao[prox-1]))
        if cor:
            return cor[0]
        else:
            return -1
    
    def GetBaldeacaoPresente(self):
        if self.pai == 0:
            return False
        if self.pai.linhaAtual == - 1 or self.pai.linhaAtual == self.linhaAtual:
            return False
        elif self.pai.linhaAtual != self.linhaAtual:
            return True
        
    def GetBaldeacaoFuturo(self):
        cor = self.encontrarLinha(self.destino)
        if cor == -1:
            return True
        return False
        
    def CriarFilhos(self):
        if not self.filhos:
            for i in estacoes_filhas[self.valor - 1]:
                proximo_valor = i
                copiaPai = deepcopy(self)
                proxLinha = self.encontrarLinha(i)
                self.filho = Estado_Atual(proximo_valor, copiaPai, self.velocidade, self.t_bald, proxLinha)
                self.filhos.append(self.filho)
                
class A_Estrela:
    
    def __init__(self, velocidade, tempoBald, inicio, destino):
        self.caminho = []
        self.nosVisitados = []
        self.tempoTotal = 0
        self.filaPrioridade = PriorityQueue()
        self.inicio = inicio
        self.destino = destino
        self.velocidade = velocidade
        self.tempoBald = tempoBald
    
    def solucao(self):
        estadoInicial = Estado_Atual(self.inicio, 0, self.velocidade, self.tempoBald, -1, self.inicio, self.destino)
        count = 0
        self.filaPrioridade.put((0, count, estadoInicial))
        while(not self.caminho and self.filaPrioridade.qsize()): #enquanto o caminho não existir e a fila de prioridade nao for vazia
            proximoEstado = self.filaPrioridade.get()[2]                    
            proximoEstado.CriarFilhos()
            self.nosVisitados.append(proximoEstado.valor)
            for t in proximoEstado.filhos:
                if t.valor not in self.nosVisitados:
                    count += 1
                    if not t.distanciaReta:
                        self.caminho = t.caminho
                        self.tempoTotal = t.tempo
                        break
                    self.filaPrioridade.put((t.custo, count, t))

        if not self.caminho:
            print("Não foi possível encontrar solução")
        return self.caminho

# MAIN

if __name__ == "__main__":

    #Recebimento de Entradas#
    
    inicio,destino = input().split(" ") # numero de nós # numero de relacoes
    inicio = int(inicio)
    destino = int(destino)
    vel = int(input())
    t_bald = int(input())
    # Fim das Entradas #
    if (inicio == destino):
        print(inicio)
        print(inicio)
        print(0.0)
    else:
        a = A_Estrela(vel, t_bald, inicio, destino)
        a.solucao()
    
        #Impressão dos Resultados
        string_caminho = ""
        string_visitados = ""
        
        for i in a.nosVisitados:
            string_visitados += str(i) + "-"
        string_visitados += str(destino)

        for i in a.caminho:
            string_caminho += str(i) + "-"
        string_caminho = string_caminho[:-1]

        print(string_visitados)
        print(string_caminho)
        print("%.1f" % a.tempoTotal)