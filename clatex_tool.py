import sys
import data # type: ignore

f = open(sys.argv[1]+".ctex","r",encoding="utf8")
full = f.read()
lines = full.split("\n")
envreplacements = data.envreplacements
mathenvreplacements = data.mathenvreplacements
englishreplacements = data.englishreplacements #⫢ is special because conjugation
replacements = data.replacements
presets = data.presets

subs = data.subs
sups = data.sups
def piecewise(line):
    newline = ""
    pwf = False
    incond = False
    cond = ""
    for c in line:
        if c=="🝑":
            newline = newline+"=⦃"
            incond = True
            pwf = True
        elif c=="🝒":
            newline = newline+"⦃"
            incond = True
            pwf = True
        elif c=="⟼" and pwf:
            incond = False
        elif c=="⬠" and pwf:
            newline = newline+"&⸢if ⸥"+cond+"\\\\"
            incond = True
            cond = ""
        elif c=="⁑" and pwf:
            newline = newline+"&⸢if ⸥"+cond+"⁑"
            pwf = False
            cond = ""
        elif incond and pwf:
            cond = cond+c
        else:
            newline = newline+c
    return newline
def lettermods(line):
    line = line+" "
    i = 0
    insub = False
    insup = False
    inund = False
    inove = False
    inhat = False
    invec = False
    newline = ""
    while(i<len(line)):
        toAdd = True
        if line[i] in subs and not insub and line[i-1] not in englishreplacements and line[i-1] not in subs:
            newline = newline+"_{"
            insub = True
        elif not(line[i] in subs) and insub:
            newline = newline+"}"
            insub = False
        if line[i] in sups and not insup and line[i-1] not in englishreplacements and line[i-1] not in sups:
            newline = newline+"^{"
            insup = True
        elif not(line[i] in sups) and insup:
            newline = newline+"}"
            insup = False
        if line[i]=="‗":
            if inund:
                newline = newline+"„"
                toAdd = False
            inund = not inund
        if line[i]=="¯":
            if inove:
                newline = newline+"„"
                toAdd = False
            inove = not inove
        if line[i]=="ㇸ":
            if inhat:
                newline = newline+"„"
                toAdd = False
            inhat = not inhat
        if line[i]=="﹋":
            if invec:
                newline = newline+"„"
                toAdd = False
            invec = not invec
        if toAdd:
            newline = newline+line[i]
        i=i+1
    return newline[:-1]
def sequences(line):
    if line[0]=="⇶":
        newline = "⁅ⓣ"
        overarrow = False
        for c in line[1:]:
            if c=="┄":
                newline = newline+"ɐ[r,\""
                overarrow = True
            elif c=="⤍":
                if overarrow:
                    newline = newline+"\"]"
                else:
                    newline = newline+"ɐ[r]"
                newline = newline+"&"
                overarrow = False
            else:
                newline = newline+c
        line = newline+"/ⓣ⁆"
    return line
def radicals(line):
    i = 0
    while i<len(line):
        if line[i]=="√":
            if line[i-1]=="]":
                layer = 1
                j = i-1
                while layer>0:
                    j = j-1
                    if line[j]=="[":
                        layer = layer-1
                    elif line[j]=="]":
                        layer = layer+1
                line = line[:j]+"√"+line[j:i]+"{"+line[i+1:]
            else:
                line = line[:i+1]+"{"+line[i+1:]
        i=i+1
    return line
def parenthesis(line):
    newline = ""
    for i,v in enumerate(line):
        if v in "([⁽󲎊₍󱼍" and line[i-5:i]!="\\left":
            newline = newline+"\\left"
        elif v in ")]₎󱼎⁾󲎋" and line[i-6:i]!="\\right":
            newline = newline+"\\right"
        newline+=v
    return newline

adjreplacements = {
    "Ⴚ": {
        "ᴬ": "abelian",
        "ᶜ": "cyclic",
        "ᴱ": "free",
        "ᴵ": "simple",
        "ᴼ": "solvable"
    },
    "ⴽ": {
        "ᶜ": "commutative",
        "ᴺ": "Noetherian",
        "ᴾ": "polynomial",
        "ᵛ": "discrete valuation",
        "ᴱ": "endomorphism"
    }
}
#󰤱 make the 󰬀 in ∀󰬀X plural, i.e., remove a(n) and add ((i)e)s
def markup(mafs,capital=True,style="inline"):
    mafs = sequences(mafs)
    mafs = lettermods(mafs)
    mafs = piecewise(mafs)
    mafs = radicals(mafs)
    mafs = parenthesis(mafs)
    newmafs = ""
    q = ""
    english = []
    space = False
    parens = 0
    for c in mafs:
        if c in "⌜([{⟨❴⦋⟬⦅⟦⦃⥏«⟪｟‹⌊⌈⸨⎩🢔⁅⢨₍󱼍󱴹󱼑󱼓󲒕󱼕󱲝󱼏󲒍󱼗󲒓󱶚󱼟󱵜󱵚󱼙󱼡⁽󲎊󲆶󲎎󲎐󲖟󲎒󲄚󲎌󲖗󲎔󲖝󲈗󲎜󲇙󲇗󲎖󲎞":
            parens=parens+1
        elif c in "⌟)]}⟩❵⦌⟭⦆⟧⦄⥑»⟫｠›⌋⌉⸩⎫🢖⁆⁑⡅₎󱼎󱴺󱼒󱼔󲒖󱼖󱲞󱼐󲒎󱼘󲒔󱶛󱼠󱵝󱵛󱼚󱼢⁾󲎋󲆷󲎏󲎑󲖠󲎓󲄛󲎍󲖘󲎕󲖞󲈘󲎝󲇚󲇘󲎗󲎟":
            parens=parens-1
        if c in englishreplacements.keys():
            erc = englishreplacements[c]
            if erc[:2]=="a ":
                english.append("a")
                english.append(erc[2:])
            else:
                english.append(erc)
            if c in "⎉⎊↘ႺⴽⱮҒƇƊᏕꝈѴᵮ":
                q = c
            elif c not in sups and c not in subs:
                q = ""
        elif c=="⫢":
            english.append("as" if q=="⎊" else "be" if q=="⎉" else "is")
        elif (c in sups or c in subs) and q not in "⎉⎊":
            if q=="↘":
                if english[-1]=="$ variables":
                    english[-2] = english[-2]+replacements[c]
                else:
                    english.append("$"+replacements[c])
                    english.append("$ variables")
                # english.append("$"+replacements[c]+"$ variables")
            else:
                english.insert(len(english)-1,adjreplacements[q][c])
        else:
            if english:
                if capital:
                    english[0] = english[0].capitalize()
                if parens==0 and style=="inline":
                    newmafs+=" $"+" "*space+" ".join(english)+" $ "
                else:
                    newmafs+="\\text{"+" "*space+" ".join(english)+" }"
                english = []
            newmafs+=replacements.get(c,c)
            capital = False
            space = True
    if english:
        if capital:
            english[0] = english[0].capitalize()
        if parens==0 and style=="inline":
            newmafs+=" $"+" "*space+" ".join(english)+" $ "
        else:
            newmafs+="\\text{"+" "*space+" ".join(english)+" }"
    return newmafs

reftext = lambda longref: longref[1:].split(":")[-1].replace(" "," ")

pieces = full.split("\\begin{document}")

newfile = pieces[0]+"\\begin{document}"

preset = lines[0]
latex_preset = presets.get(preset,lines[0])
newfile = latex_preset+newfile[len(lines[0]):]

prevspace = 0
longmath = False
env = []
shortmath = False
charmath = False
mafs = ""
pc = ""
capital = True
reference = ""
onlyspace = True
for c in pieces[1]:
    onlyspace = c=="\n" or onlyspace and c in " \t"
    if c=="﹩":
        shortmath = True
        newfile = newfile+"$"
    elif c=="💲":
        if longmath:
            newfile = newfile+markup(mafs,capital,"block")
            mafs = ""
        longmath = not longmath
        newfile = newfile+"$$"
    elif c=="$" and pc!="\\" and pc!="$":
        longmath = not longmath
        newfile = newfile+"$"
    elif c=="$" and pc=="$":
        newfile = newfile+"$"
    elif c=="¢":
        charmath = True
    elif charmath:
        charmath = False
        newfile = newfile+"$"+markup(c,capital,"character")+"$"
    elif c in envreplacements.keys():
        newfile = newfile+"\\begin{"+envreplacements[c]+"}"
        env.append(envreplacements[c])
    elif c in mathenvreplacements.keys():
        longmath = True
        newfile = newfile+"\\begin{"+mathenvreplacements[c]+"}"
        env.append(mathenvreplacements[c])
    elif c=="☠":
        if longmath:
            newfile = newfile+markup(mafs,capital,"block")
            mafs = ""
            longmath = False
        newfile = newfile+"\\end{"+env.pop()+"}"
    elif c in " \n" and shortmath:
        marked = markup(mafs,capital)
        punctuation = ""
        if marked[-1] in ".?,:":
            punctuation = marked[-1]
            marked = marked[:-1]
        newfile = newfile+marked+"$"+punctuation+c
        mafs = ""
        shortmath = False
        prevspace = len(newfile)-1
        capital = punctuation in ".?" or onlyspace # capital = punctuation in ".?"
    elif (longmath or shortmath) and c!="\n":
        mafs = mafs+c
    elif c in replacements.keys() or c in englishreplacements.keys():
        mafs = newfile[prevspace+1:]+c
        newfile = newfile[:prevspace+1]+" $"
        shortmath = True
    elif c==" ":
        if len(reference):
            newfile = newfile+reftext(reference)
            reference = ""
        prevspace = len(newfile)
        newfile = newfile+c
        capital = pc in ".?!]⊢" or onlyspace
    elif longmath and c=="\n":
        prevspace = len(newfile)
        mafs = mafs+c
    elif c=="\n":
        if len(reference):
            newfile = newfile+reftext(reference)
            reference = ""
        prevspace = len(newfile)
        newfile = newfile+c
        capital = True # capital = pc in "\n{.?!"
    elif c=="⊢":
        prevspace = len(newfile)
        newfile = newfile+"\\item "
    elif c=="󰤱":
        prevspace = len(newfile)
        newfile = newfile+"%"
    elif c=="ꔧ":
        reference = "ꔧ"
    elif len(reference):
        reference = reference+c
    else:
        newfile = newfile+c
    pc = c
#cleanup empty $ $ and stuff
newfile = newfile.replace("$ $","")
newfile = newfile.replace(" .",".")
newfile = newfile.replace(" "," ")
newfile = newfile.replace("  "," ")
#liminf and limsup fixer
newfile = newfile.replace("\\lim \\sup ","\\limsup ")
newfile = newfile.replace("\\lim \\inf ","\\liminf ")

print(newfile)

f.close()
