# Group 04 — Nupe (Nupeci) — HW1 submission import numpy as np

class BigramModel:
    """A simple bigram language model."""
    
    def __init__(self):
        self.bigrams = {}
        self.vocab_size = 0
    
    def fit(self, corpus_path):
        """Train the model on a corpus file."""
        self.bigrams = {}
        words = []
        
        with open(corpus_path, 'r', encoding='utf-8') as f:
            for line in f:
                line_words = line.strip().split()
                words.extend(line_words)
        
        self.vocab_size = len(set(words))
        
        for i in range(len(words) - 1):
            bigram = (words[i], words[i + 1])
            self.bigrams[bigram] = self.bigrams.get(bigram, 0) + 1
        
        return len(self.bigrams)
    
    def compute_perplexity(self, test_path):
        """Calculate perplexity on a test file."""
        words = []
        
        with open(test_path, 'r', encoding='utf-8') as f:
            for line in f:
                line_words = line.strip().split()
                words.extend(line_words)
        
        if len(words) < 2:
            return 1.0
        
        log_prob = 0.0
        bigram_count = 0
        
        for i in range(len(words) - 1):
            bigram = (words[i], words[i + 1])
            
            if bigram in self.bigrams:
                prob = self.bigrams[bigram] / sum(self.bigrams.values())
            else:
                prob = 1e-10
            
            log_prob += -np.log(prob)
            bigram_count += 1
        
        perplexity = np.exp(log_prob / bigram_count)
        return perplexity
