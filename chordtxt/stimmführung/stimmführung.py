"""
Es soll für vorgegebene akkordverbindungen anhand von stimmführungsregeln optimieren.
Beispiel für eine vorgegebene Akkordverbindung:
['C3 C4 E4 G4', 'D3 D4 F4 A4 C5', 'E3 C4 E4 G4', 'D3 D4 F4 A4 C5']
Stimmführungsregeln:
- Gemeinsame Töne zweier aufeinander folgender Akkorde bleiben in der gleichen Stimme liegen (Ligatur).
- Wenn keine Ligatur möglich ist, werden die Stimmen möglichst stufenweise geführt.
- Die Oberstimme wird vorzugsweise aufwärts, die Unterstimme abwärts geführt (Kontrabewegung).
- Parallelbewegungen von Quinten und Oktaven sind zu vermeiden, ebenso die direkte Führung in diese Intervalle.
- Die Terz und die Septime eines Akkordes werden in der Regel aufgelöst, d.h. sie werden in die nächste Stufe geführt.
- Die Leitton (die Septime der Dominante) wird in der Regel zur Tonika geführt, die Unterleitton (die Sexte der Subdominante) zur Dominante.
- Die Stimmen sollen einen möglichst gleichmäßigen Ambitus einhalten und nicht zu weit auseinander liegen oder sich kreuzen.
"""