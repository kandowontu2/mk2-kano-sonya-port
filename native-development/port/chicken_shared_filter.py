"""Bounded prefix-only shared FIR experiment; no claim about the real mixer."""
import numpy as np

def fit_shared_filter(observed,prediction,training):
    assert observed.ndim==prediction.ndim==training.ndim==1
    assert observed.shape==prediction.shape==training.shape
    assert len(observed)<=15*48000 and training.dtype==bool
    offsets=np.arange(-4,5)
    valid=np.ones(len(observed),dtype=bool);valid[:4]=False;valid[-4:]=False
    positions=np.flatnonzero(training & valid)
    assert len(positions)>36
    features=prediction[positions[:,None]+offsets]
    coefficients,_,rank,singular=np.linalg.lstsq(features,observed[positions],rcond=1e-10)
    assert rank==9,'Shared filter is not identified by training prefixes'
    filtered=np.zeros_like(prediction,dtype=float)
    end=len(prediction)-4
    for coefficient,offset in zip(coefficients,offsets):
        filtered[4:end]+=coefficient*prediction[4+offset:end+offset]
    return filtered,valid,dict(taps=9,offsetSamples=offsets.tolist(),coefficients=coefficients.tolist(),
        trainingSamples=len(positions),rank=int(rank),featureBytes=int(features.nbytes),
        conditionNumber=float(singular[0]/singular[-1]),fittedOnlyOnTrainingPrefixes=True,
        observedValidationSamplesUsedForFitting=False,nativeMixerMechanismProven=False)
