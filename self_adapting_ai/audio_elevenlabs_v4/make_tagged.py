"""Insert short ElevenLabs audio tags before chosen sentences; text is otherwise verbatim from VOICEOVER_SCRIPT_V2.md."""
import sys
sys.path.insert(0, "../m3b/voice")
from direction import script_chapters
TAGS = {
 2: {"To understand our architectural": "[curious]", "A human brain operates": "[excited]", "Crucially, the biological": "[serious]",
     "Under the governing laws": "[excited]", "Now compare this living": "[sighs]", "Why couldn't our artificial": "[curious]"},
 3: {"The dream of self-adapting": "[curious]", "In 1949, Canadian": "[excited]", "In 1982, Finnish": "[excited]",
     "The self-organizing hypothesis was": "[excited]", "For decades, this": "[serious]", "Yet when these ideas": "[sighs]"},
}

TAGS.update({
 4: {"This brings us to the core": "[serious]", "And conversely, why did": "[curious]", "Examine the stark contradiction": "[serious]",
     "Meanwhile, the Transformer": "[excited]", "How could a rigid": "[curious]", "To understand why self-adapting": "[serious]"},
 5: {"Our first theoretical barrier": "[serious]", "When we analyze the dynamical": "[serious]", "In formal terms:": "[dramatic]",
     "Now look at what is fundamentally": "[curious]", "In a Transformer, the attention": "[excited]", "Local Hebbian rewiring is": "[serious]"},
 6: {"Our second fundamental barrier": "[serious]", "What does this lower bound": "[curious]", "It must traverse": "[serious]",
     "In stark contrast": "[excited]", "Every single token attends": "[excited]"},
 7: {"Our third and most": "[serious]", "In 2019, artificial": "[curious]", "Now examine what happens": "[serious]",
     "We measured it on this": "[excited]", "Furthermore, consider credit": "[serious]", "Without global backpropagation": "[sighs]"},
 8: {"To test these theorems": "[excited]", "The results were unequivocal.": "[dramatic]", "For the first forty epochs": "[serious]",
     "The Transformer, meanwhile": "[excited]", "The theory survived": "[excited]"},
 9: {"Recognizing these fundamental": "[curious]", "Instead, they engineered": "[excited]", "Notice how this resolves": "[excited]",
     "Modularity is alive": "[excited]"},
 10: {"So far, this has been": "[sighs]", "That is Hebb's rule.": "[excited]", "In 2021, Imanol": "[curious]",
      "So the Transformer never": "[excited]", "We tested this on": "[excited]", "Self-adapting intelligence did": "[excited]"},
 11: {"Before we look ten": "[curious]", "The first idea:": "[excited]", "The second idea:": "[curious]", "The third idea:": "[excited]",
      "And the fourth:": "[curious]", "If any of these": "[excited]"},
 12: {"Where does this leave": "[curious]", "The true frontier": "[excited]", "First, Neuromorphic": "[excited]",
      "As hardware designers": "[excited]", "Yet the artificial minds": "[serious]", "Thank you for joining": "[excited]"},
})
S = script_chapters()
for n in map(int, sys.argv[1:]):
    t = S[n]
    for k, tag in TAGS[n].items():
        assert t.count(k) == 1, (n, k)
        t = t.replace(k, f"{tag} {k}")
    open(f"tagged/ch{n:02d}.txt", "w").write(t + "\n")
