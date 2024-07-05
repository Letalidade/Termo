package cu;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import java.util.Scanner;

public class termogame {

    /**
     * Método para obter o idioma escolhido pelo usuário (P para Português, I para Inglês).
     */
    public static String obterIdioma(Scanner scanner) {
        while (true) {
            System.out.print("Qual o idioma (I para inglês ou P para português)? ");
            String idioma = scanner.nextLine().strip().toUpperCase();
            if (idioma.equals("I") || idioma.equals("P")) {
                return idioma;
            }
            System.out.println("Entrada inválida! Por favor, digite 'I' para inglês ou 'P' para português.");
        }
    }

    /**
     * Método para criar uma lista de palavras a partir de um arquivo.
     */
    public static List<String> criaListaPalavras(String nomeArquivo) throws IOException {
        List<String> palavras = new ArrayList<>();
        try (BufferedReader reader = new BufferedReader(new FileReader(nomeArquivo))) {
            String linha;
            while ((linha = reader.readLine()) != null) {
                palavras.add(linha.trim());
            }
        }
        return palavras;
    }

    /**
     * Método para comparar letras, removendo acentos e convertendo para minúsculas.
     */
    public static String compararLetras(String texto) {
        String textoNormalizado = Normalizer.normalize(texto, Normalizer.Form.NFD);
        textoNormalizado = textoNormalizado.replaceAll("[^\\p{ASCII}]", "");
        return textoNormalizado.toLowerCase();
    }

    /**
     * Método para checar a tentativa do jogador.
     */
    public static int[] checaTentativa(String palavra, String chute) {
        int[] feedback = new int[5];
        String palavraVerificada = compararLetras(palavra);
        String chuteVerificado = compararLetras(chute);

        char[] letrasDisponiveis = palavraVerificada.toCharArray();

        for (int i = 0; i < 5; i++) {
            if (chuteVerificado.charAt(i) == palavraVerificada.charAt(i)) {
                feedback[i] = 1;
                letrasDisponiveis[i] = ' '; // Remove a letra usada
            }
        }

        for (int i = 0; i < 5; i++) {
            if (feedback[i] == 0 && palavraVerificada.contains(String.valueOf(chuteVerificado.charAt(i)))) {
                feedback[i] = 2;
                letrasDisponiveis[palavraVerificada.indexOf(chuteVerificado.charAt(i))] = ' '; // Remove a letra usada
            }
        }

        return feedback;
    }

    /**
     * Método para atualizar o teclado, substituindo letras inexistentes por espaços.
     */
    public static void atualizaTeclado(String chute, int[] feedback, String[] teclado) {
        String chuteVerificado = compararLetras(chute);

        for (int i = 0; i < 5; i++) {
            if (feedback[i] == 0) {
                char tecla = chuteVerificado.charAt(i);
                for (int linha = 0; linha < teclado.length; linha++) {
                    teclado[linha] = teclado[linha].replace(tecla, ' ');
                }
            }
        }
    }

    /**
     * Método para imprimir o resultado das tentativas.
     */
    public static void imprimeResultado(List<String[]> listaTentativas) {
        for (String[] tentativa : listaTentativas) {
            System.out.println(tentativa[0]);
            System.out.println(tentativa[1]);
        }
    }

    /**
     * Método principal do jogo.
     */
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        String idioma = obterIdioma(scanner);
        String nomeArquivo = idioma.equals("I") ? "words.txt" : "palavras.txt";

        List<String> palavras;
        try {
            palavras = criaListaPalavras(nomeArquivo);
        } catch (IOException e) {
            System.out.println("Erro ao ler o arquivo de palavras.");
            return;
        }

        List<String> palavrasNormalizadas = new ArrayList<>();
        for (String palavra : palavras) {
            palavrasNormalizadas.add(compararLetras(palavra));
        }

        Random random = new Random();
        String palavraSorteada = palavras.get(random.nextInt(palavras.size()));
        String palavraSorteadaNormalizada = compararLetras(palavraSorteada);

        String[] teclado = {"q w e r t y u i o p", "a s d f g h j k l ", "z x c v b n m"};
        List<String[]> listaTentativas = new ArrayList<>();

        boolean ganhou = false; // Indica se o jogador ganhou o jogo

        for (int tentativa = 0; tentativa < 6; tentativa++) {
            System.out.println("---------------------------------------------------------------");
            for (String linha : teclado) {
                System.out.println(linha);
            }
            System.out.println("---------------------------------------------------------------");
            imprimeResultado(listaTentativas);

            System.out.print("Digite a palavra: ");
            String chute = scanner.nextLine().trim().toLowerCase();

            String chuteNormalizado = compararLetras(chute);

            if (chute.length() != 5 || !palavrasNormalizadas.contains(chuteNormalizado)) {
                System.out.println("Palavra inválida!");
                continue;
            }

            int[] feedback = checaTentativa(palavraSorteadaNormalizada, chuteNormalizado);
            listaTentativas.add(new String[]{chute, feedbackToString(feedback)});

            atualizaTeclado(chute, feedback, teclado);

            if (chuteNormalizado.equals(palavraSorteadaNormalizada)) {
                ganhou = true;
                imprimeResultado(listaTentativas);
                System.out.println("PARABÉNS!");
                break;
            }
        }

        if (!ganhou) {
            imprimeResultado(listaTentativas);
            System.out.println("Você perdeu. A palavra era " + palavraSorteada + ".");
        }

        scanner.close();
    }

    /**
     * Método auxiliar para converter o array de feedback em uma string formatada.
     */
    public static String feedbackToString(int[] feedback) {
        StringBuilder sb = new StringBuilder();
        for (int i : feedback) {
            sb.append(i);
        }
        return sb.toString();
    }
}
