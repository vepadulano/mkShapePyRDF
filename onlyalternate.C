// Function substitute for ROOT's Alt$ special function of the TTree::Draw method.
template
<typename container>
float alternate(container c, int index, float alt){
   if (index < c.size()) {
        return c[index];
   }
   else{
        return alt;
   }
}

void onlyalternate(){
   ROOT::RDataFrame df("Events","nanoLatino_DYJetsToLL_M-50-LO__part3.root");


   // Define bVeto and btag0 aliases
   // Filter only with supercut
   // Create histogram from ZEE.njet variable
   // Note that "njet" throws errors because is already defined in the tree
   // so it was changed to "newnjet"
   auto njet_hist = df.Define("bVeto",
                              "auto condition_vec = (CleanJet_pt > 20. && abs(CleanJet_eta)<2.5 && Jet_btagDeepB[CleanJet_jetIdx] > 0.1241);\
                               return std::accumulate(condition_vec.begin(), condition_vec.end(), 0) == 0;")
                       .Define("btag0",
                               "auto condition_vec = (CleanJet_pt > 20. && abs(CleanJet_eta)<2.5 && Jet_btagDeepB[CleanJet_jetIdx] > 0.1241);\
                                return alternate(CleanJet_pt, 0, 0) < 30 && std::accumulate(condition_vec.begin(), condition_vec.end(), 0) > 0;")
                       .Filter("mll>60 && Lepton_pt[0]>20 && Lepton_pt[1]>10 && (nLepton>=2 && alternate(Lepton_pt, 2, 0)<10) \
                                && abs(Lepton_eta[0])<2.5 && abs(Lepton_eta[1])<2.5")
                       .Filter("(Lepton_pdgId[0] * Lepton_pdgId[1] == -11*11) && Lepton_pt[0]>25 && Lepton_pt[1]>13 && mll>60 && mll<120 ;")
                       .Define("newnjet",
                               "auto condition_vec = CleanJet_pt > 15;\
                                return std::accumulate(condition_vec.begin(), condition_vec.end(), 0);")
                       .Histo1D({"njet","njet", 5, 0, 5}, {"newnjet"});


   TCanvas c("njet","njet", 800,700);
   njet_hist->Draw();
   c.SaveAs("img_njet.png");
}
