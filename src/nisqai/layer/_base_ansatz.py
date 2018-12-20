#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

"""Module with basic ansatz class definitions to be inherited by other
ansatz classes.
"""

from pyquil import Program

class BaseAnsatz():
    """Base ansatz for all ansatz classes."""
    
    def __init__(self, num_qubits):
        self._num_qubits = num_qubits
        self.circuit = Program()

    @property
    def num_qubits(self):
        """Returns the number of qubits in the ansatz."""
        return self._num_qubits

    def depth(self):
        """Computes the depth of the circuit ansatz.
        
        Here, the depth is the maximum number of "incompressible" operations
        over all qubits.
        """
        # TODO: complete method
        # TODO: make gate_alphabet an argument (probably write a gate_alphabet
        # class)
        pass

    def num_ops(self, qubits):
        """Returns the total number of operations over a subset of qubits
        in the circuit ansatz.
        """
        # TODO: complete method
        # TODO: make gate_alphabet an argument (probably write a gate_alphabet
        # class)
        pass

    def __str__(self):
        """Returns a circuit diagram."""
        # TODO: complete method
        # probably want to write a TextDiagramDrawer class like in Cirq
        return self.circuit.__str__()