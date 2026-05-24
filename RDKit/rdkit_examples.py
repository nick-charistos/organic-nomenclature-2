import os
try:
    from rdkit import Chem
    from rdkit.Chem import Draw
    from rdkit.Chem import Descriptors
    from rdkit.Chem import AllChem
    from rdkit.Chem import rdMolDescriptors
    from rdkit.Chem import Lipinski
except ImportError:
    print("Σφάλμα: Η βιβλιοθήκη RDKit δεν είναι εγκατεστημένη.")
    print("Παρακαλώ τρέξτε: pip install rdkit")

# 1. Δημιουργία Μορίου από SMILES (Simplified Molecular Input Line Entry System)
# Η Ασπιρίνη (Acetylsalicylic acid)
aspirin_smiles = "CC(=O)OC1=CC=CC=C1C(=O)O"
mol_aspirin = Chem.MolFromSmiles(aspirin_smiles)
aspirin_smiles = "O=C(C)Oc1ccccc1C(=O)O"
mol_aspirin = Chem.MolFromSmiles(aspirin_smiles)
print(mol_aspirin)

print(f"Ασπιρίνη - Αριθμός ατόμων (χωρίς H): {mol_aspirin.GetNumAtoms()}")

# 2. Οπτικοποίηση και Αποθήκευση Εικόνας
# Αποθηκεύει το μόριο ως αρχείο PNG για χρήση σε εργασία
Draw.MolToFile(mol_aspirin, 'aspirin_structure.png', size=(300, 300))
print("Η δομή της Ασπιρίνης αποθηκεύτηκε ως 'aspirin_structure.png'")

# 3. Υπολογισμός Φυσικοχημικών Ιδιοτήτων
mw = Descriptors.MolWt(mol_aspirin)
logp = Descriptors.MolLogP(mol_aspirin)
h_donors = Lipinski.NumHDonors(mol_aspirin)
h_acceptors = Lipinski.NumHAcceptors(mol_aspirin)

print("\n--- Ιδιότητες Ασπιρίνης ---")
print(f"Μοριακό Βάρος: {mw:.2f} g/mol")
print(f"Συντελεστής Κατανομής (LogP): {logp:.2f}")
print(f"Δότες Δεσμών Η: {h_donors}")
print(f"Δέκτες Δεσμών Η: {h_acceptors}")

# 4. Διαχείριση Λίστας Μορίων (Πίνακας)
#Τόσο ο Κανόνας του Lipinski όσο και το $\log P$ είναι θεμελιώδεις έννοιες στη
#Φαρμακευτική Χημεία και τη Χημειοπληροφορική. Χρησιμοποιούνται για να
#προβλέψουν αν ένα μόριο που ανακαλύπτουμε στο εργαστήριο μπορεί να λειτουργήσει
#αποτελεσματικά ως φάρμακο που λαμβάνεται από το στόμα (χάπι/κάψουλα).
#Το $\log P$ είναι το μέτρο της λιποφιλικότητας μιας χημικής ένωσης (πόσο "αγαπάει" τα λίπη ή το νερό).
smiles_list = {
    'Καφεΐνη': 'CN1C=NC2=C1C(=O)N(C(=O)N2C)C',
    'Ιβουπροφαίνη': 'CC(C)CC1=CC=C(C=C1)C(C)C(=O)O',
    'Αιθανόλη': 'CCO',
    'Νικοτίνη': 'CN1CCCC1C2=CN=CC=C2'
}

mols = [Chem.MolFromSmiles(s) for s in smiles_list.values()]
img = Draw.MolsToGridImage(mols, molsPerRow=2, subImgSize=(300, 300), legends=list(smiles_list.keys()))
img.save('molecule_grid.png')
print("\nΤο πλέγμα μορίων αποθηκεύτηκε ως 'molecule_grid.png'")

# 5. Αναζήτηση Υποδομής (Substructure Search)
# Ψάχνουμε αν το μόριο περιέχει βενζολικό δακτύλιο
benzene_pattern = Chem.MolFromSmarts("c1ccccc1")
for name, smiles in smiles_list.items():
    m = Chem.MolFromSmiles(smiles)
    has_benzene = m.HasSubstructMatch(benzene_pattern)
    print(f"Το μόριο {name} {'περιέχει' if has_benzene else 'ΔΕΝ περιέχει'} βενζόλιο.")

# 6. Έλεγχος "Κανόνα των 5" (Drug-likeness)
def check_lipinski(mol):
    conditions = [
        Descriptors.MolWt(mol) <= 500,
        Descriptors.MolLogP(mol) <= 5,
        rdMolDescriptors.CalcNumHBD(mol) <= 5,
        rdMolDescriptors.CalcNumHBA(mol) <= 10
    ]
    return all(conditions)

print(f"\nΗ Ιβουπροφαίνη ακολουθεί τον κανόνα Lipinski; {check_lipinski(mols[1])}")

# 7. Ταυτοποίηση Λειτουργικών Ομάδων
# Χρησιμοποιούμε SMARTS patterns για καρβοξυλικά οξέα [-C(=O)OH]
acid_pattern = Chem.MolFromSmarts("C(=O)[OH]")
aspirin_acid = mol_aspirin.GetSubstructMatches(acid_pattern)
print(f"Η Ασπιρίνη περιέχει {len(aspirin_acid)} καρβοξυλική ομάδα.")

# 8. Παραγωγή 3D Συντεταγμένων και αποθήκευση σε αρχείο
# Προσθήκη υδρογόνων και παραγωγή 3D δομής
mol_3d = Chem.AddHs(mol_aspirin)
AllChem.EmbedMolecule(mol_3d, AllChem.ETKDG())
print("\nΠαρήχθησαν 3D συντεταγμένες για την Ασπιρίνη.")
# print(Chem.MolToMolBlock(mol_3d)) # Εμφάνιση του αρχείου .mol
Chem.MolToMolFile(mol_3d, 'aspirin_3d.mol')

"""
Συμβουλές για τους Φοιτητές:
1. Τα SMILES είναι ο πιο εύκολος τρόπος να "μεταφέρετε" χημεία στον υπολογιστή.
2. Μπορείτε να βρείτε τα SMILES οποιουδήποτε μορίου στο PubChem ή στη Wikipedia.
3. Η RDKit είναι πανίσχυρη. Συνδυάστε την με το Pandas για να αναλύσετε χιλιάδες μόρια ταυτόχρονα!
"""
