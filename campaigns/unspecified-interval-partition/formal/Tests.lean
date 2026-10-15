import Challenge
open UnspecifiedIntervalPartition
example : targetWitness (⟨2,[(0,1)]⟩,2) ([0,1],[(0,1),(1,2)]) = true := by native_decide
example : targetWitness (⟨2,[(0,1)]⟩,2) ([0,0],[(0,1),(1,2)]) = false := by native_decide
