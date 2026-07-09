"""
Student Behaviour Pattern Detector 

IDEA
====

Every student is modelled as a STRING over the alphabet: 

    Sigma = { login, study, quiz, logout }

e.g. a session might look like: ["login", "study", "quiz", "logout"]

We build a Deterministic Finite Automaton (DFA) that "reads" this string action-by-action and ends up
in exactly one final state. Thata final state tells us whether the session was: 

    - SAFE : student logged in, engaged with the material 
                (studied and/or attempted the quiz), then logged out.
    - AT-RISK : student logged in and logged out WITHOUT ever attempting the quiz. 
                (The pattern we want to flag).
    - INVALID : the sequence is not physically possible (e.g. quiz before login, logging in twice, activity after logout).
    - INCOMPLETE : the string ended mid-session (no logout yet) - not enough information to classify.


FORMAL DEFINITION (5-tuple: Q, Sigma, delta, q0, F)
===================================================

Q = { q0, q1, q2, q_safe, q_risk, q_dead }
Sigma = { login, study, quiz, logout }
q0 = start state ("not logged in")
F = { q_safe }      <- the only ACCEPTING state
delta = transition function, see TRANSITION table below.

"""

from dataclasses import dataclass
from typing import List, Dict

STATES: Dict[str, str] = {
    "q0": "Not logged in (START state)",
    "q1": "Logged in, no study/quiz activity yet", 
    "q2": "Has studied, quiz NOT attempted", 
    "q3": "Quiz attempted at least once",
    "q_safe": "Session ended safely (ACCEPTING state)",
    "q_risk": "Session ended AI-RISK (logged out, no quiz attempt", 
    "q_dead": "Invalid / malformed sequence (trap state)",
    }

ALPHABET = {"login", "study", "quiz", "logout"}
START_STATE = "q0"
ACCEPTING_STATES = {"q_safe"}

TRANSITIONS: Dict[str, Dict[str, str]] = {
    "q0": {"login": "q1", "study": "q_dead", "quiz": "q_dead", "logout": "q_dead"},
    "q1": {"login": "q_dead", "study": "q2", "quiz": "q3", "logout": "q_risk"},
    "q2": {"login": "q_dead", "study": "q2", "quiz": "q3", "logout": "q_risk"},
    "q3": {"login": "q_dead", "study": "q3", "quiz": "q3", "logout": "q_safe"},
    "q_safe": {"login": "q1", "study": "q_dead", "quiz": "q_dead", "logout": "q_dead"},
    "q_risk": {"login": "q_dead", "study": "q_dead", "quiz": "q_dead", "logout": "q_dead"},
    "q_dead": {"login": "q_dead", "study": "q_dead", "quiz": "q_dead", "logout": "q_dead"},
    }

@dataclass 
class SimulationResult: 
    sequence: List[str]
    path: List[str]
    final_state: str
    label: str
    
def run_dfa(sequence: List[str]) -> SimulationResult:
    """Feed a sequence of actions through the DFA and return the result."""
    state = START_STATE
    path = [state]
    
    for symbol in sequence: 
        if symbol not in ALPHABET:
            raise ValueError(f"'{symbol}' is not in the alphabet {ALPHABET}")
        state = TRANSITIONS[state][symbol]
        path.append(state)
        
        
    if state== "q_dead": 
        label = "INVALID sequence"
    elif state == "q_safe":
        label = "SAFE - engaged studnet"
    elif state == "q_risk": 
        label = "AT-RISK - never attempted the quiz"
    else: 
        label = "INCOMPLETE - session still open (no logout yet)"
        
    return SimulationResult(sequence, path, state, label) 



def print_result(result: SimulationResult) -> None: 
    seq_str = " -> ".join(result.sequence) if result.sequence else "(empty)"
    path_str = " -> ".join(result.path)
    print(f" Sequence: {seq_str}")
    print(f" Path: {path_str}")
    print(f" Verdict : {result.label}")
    print("-" * 70)


def detect_at_risk_students(class_logsd: Dict[str, List[str]]) -> List[str]:
    
    """ 
    class_logs: { student_id : [action, action, ....], ...}
    Returns a list of student IDs whose session was classified AT-RISK.
    """
    
    at_risk = []
    for student_id, actions in class_logs.items(): 
        result = run_dfa(actions)
        if result.final_state == "q_risk": 
            at_risk.append(student_id)
    return at_risk

if __name__ == "__main__": 
    print("=" * 70)
    print("STUDENT BEHAVIOUR PATTERN DETECTOR -DFA DEMO")
    print("=" * 70)
    
    test_sequences = [
        ["login", "study", "quiz", "logout"],
        ["login", "quiz", "logout"],
        ["login", "study", "study", "quiz", "logout"],
        ["login", "logout"], 
        ["login", "study", "logout"],
        ["login", "study", "study", "logout"],
        ["quiz", "login", "logout"],
        ["login", "login", "quiz", "logout"],
        ["login", "study", "quiz"],
    ]

    for seq in test_sequences: 
        print_result(run_dfa(seq))
        
        
    print("\nBATCH DEMO - scanning a class of students\n")
    class_logs = {
        "STU_101": ["login", "study", "quiz", "logout"],
        "STU-102": ["login", "study", "logout"],
        "STU-103": ["login", "logout"],
        "STU-104": ["login", "quiz", "quiz", "logout"],
        "STU-105": ["login", "study", "quiz", "logout"],
        }
    
    flagged = detect_at_risk_students(class_logs)
    print(f"At-risk students flagged by the DFA: {flagged}")
    
    print("\nSTATE DESCRIPTION")
    print("-" * 70)
    for state, desc in STATES.items(): 
        marker = " (ACCEPTING)" if state in ACCEPTING_STATES else ""
        print(f" {state:8s}: {desc}{marker}")







