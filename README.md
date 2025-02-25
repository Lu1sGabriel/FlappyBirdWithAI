# Flappy Bird with AI

![Flappy Bird with AI](https://media1.tenor.com/m/WuaZ4G33BBoAAAAC/flappy-bird-flying.gif)

## 🚀 Descrição do Projeto

**Flappy Bird with AI** é um projeto de jogo desenvolvido em Python utilizando a biblioteca Pygame. Neste projeto, uma Rede Neural é utilizada para treinar um pássaro a navegar por canos de altura variável, aprimorando suas habilidades ao longo do tempo. Este projeto explora conceitos avançados de **inteligência artificial** e **machine learning** aplicados a jogos.

## 🛠️ Funcionalidades

- **IA Aprendendo a Jogar**: O pássaro é controlado por uma rede neural que se adapta e melhora continuamente sua performance.
- **Animação Fluida do Pássaro**: Implementação de sprites com animação suave, incluindo rotação do pássaro conforme sua velocidade vertical.
- **Detecção de Colisões Precisa**: Utilização de máscaras de colisão para garantir interações realistas entre o pássaro e os obstáculos.

## 📦 Tecnologias Utilizadas

- **Python**: A linguagem principal utilizada para o desenvolvimento do jogo.
- **Pygame**: Biblioteca para criação de jogos, gerenciamento de gráficos e eventos.
- **NEAT-Python**: Algoritmo de neuroevolução utilizado para treinar a rede neural do pássaro.

## 🔧 Estrutura do Projeto

```plaintext
src/
├── main/
│   ├── bird.py            # Implementação da classe Bird
│   ├── config.py          # Configurações do jogo
│   ├── constants.py       # Constantes do jogo
│   ├── floor.py           # Implementação da classe Floor
│   ├── main.py            # Arquivo principal do jogo
│   └── pipe.py            # Implementação da classe Pipe
└── resources/
    ├── iaSettings/
    │   └── config.txt     # Configurações da IA
    └── images/
        ├── base.png       # Imagem da base
        ├── bg.png         # Imagem do fundo
        ├── bird1.png      # Imagem do pássaro 1
        ├── bird2.png      # Imagem do pássaro 2
        ├── bird3.png      # Imagem do pássaro 3
        └── pipe.png       # Imagem do cano
```

## 🔍 Melhorias Futuras

Embora a base do projeto esteja completa e funcionando a 100%, há diversas melhorias e funcionalidades que podem ser implementadas:

- **Otimização da Rede Neural**: Refinar os parâmetros da rede para melhorar a taxa de sucesso do pássaro.
- **Estratégias de Tomada de Decisão**: Introduzir técnicas mais avançadas de aprendizado por reforço para melhorar a lógica de decisão.
- **Adaptação a Diferentes Configurações de Cano**: Variações nos padrões de canos para aumentar a dificuldade do jogo.
- **Feedback Visual e Estatísticas**: Adicionar métricas de desempenho e feedback visual para observar o aprendizado da IA.

## 🎮 Como Jogar

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/Lu1sGabriel/FlappyBirdWithAI.git
   cd FlappyBirdWithAI
   ```

2. **Instale as dependências**:
   ```bash
   pip install pygame
   ```

3. **Execute o jogo**:
   ```bash
   python main.py
   ```

## 🌐 Link para o Projeto

[Flappy Bird with AI no GitHub](https://github.com/Lu1sGabriel/FlappyBirdWithAI)

## 💬 Feedback

Estou ansioso para receber feedback e discutir sobre este projeto. Sinta-se à vontade para abrir uma issue ou um pull request!
