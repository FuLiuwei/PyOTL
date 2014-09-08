"""
Copyright (C) 2014, 申瑞珉 (Ruimin Shen)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
import math
import unittest
import numpy
import scipy.stats
import pyotl.utility
import pyotl.problem.real
import pyotl.initial.real
import pyotl.crossover.real
import pyotl.mutation.real
import pyotl.optimizer.real
import pyotl.indicator

class TestCase(unittest.TestCase):
	def setUp(self):
		self.pathData = os.path.join(os.path.dirname(__file__), 'Data')
		self.repeat = 30
	
	def tearDown(self):
		pass
	
	def testISNPS(self):
		random = pyotl.utility.Random()
		problemGen = lambda: pyotl.problem.real.DTLZ2(3)
		problem = problemGen()
		pathProblem = os.path.join(self.pathData, type(problem).__name__, str(problem.GetNumberOfObjectives()))
		_crossover = pyotl.crossover.real.SimulatedBinaryCrossover(random, 1, problem.GetBoundary(), 20)
		crossover = pyotl.crossover.real.CoupleCoupleCrossoverAdapter(_crossover, random)
		mutation = pyotl.mutation.real.PolynomialMutation(random, 1 / float(len(problem.GetBoundary())), problem.GetBoundary(), 20)
		boundaryMatrix = numpy.loadtxt(os.path.join(pathProblem, 'Boundary.csv'))
		lower, _ = boundaryMatrix.T
		lower = pyotl.utility.PyList2Vector_Real(lower.tolist())
		angle1 = 2.3 * math.pi / 180
		angle2 = 45 * math.pi / 180
		amplification = 3
		pfList = []
		for _ in range(self.repeat):
			problem = problemGen()
			initial = pyotl.initial.real.PopulationUniform(random, problem.GetBoundary(), 100)
			convergenceDirection = pyotl.utility.PyList2BlasVector_Real([1] * problem.GetNumberOfObjectives())
			optimizer = pyotl.optimizer.real.ISNPS(random, problem, initial, crossover, mutation, lower, convergenceDirection, angle1, angle2, amplification)
			while optimizer.GetProblem().GetNumberOfEvaluations() < 30000:
				optimizer()
			pf = pyotl.utility.PyListList2VectorVector_Real([list(solution.objective_) for solution in optimizer.GetSolutionSet()])
			pfList.append(pf)
		pathCrossover = os.path.join(pathProblem, type(crossover.GetCrossover()).__name__)
		pathOptimizer = os.path.join(pathCrossover, type(optimizer).__name__)
		pfTrue = pyotl.utility.PyListList2VectorVector_Real(numpy.loadtxt(os.path.join(pathProblem, 'PF.csv')).tolist())
		#GD
		indicator = pyotl.indicator.DTLZ2GD()
		metricList = [indicator(pf) for pf in pfList]
		rightList = numpy.loadtxt(os.path.join(pathOptimizer, 'GD.csv')).tolist()
		self.assertGreater(scipy.stats.ttest_ind(rightList, metricList)[1], 0.05, [numpy.mean(rightList), numpy.mean(metricList), metricList])
		#IGD
		indicator = pyotl.indicator.InvertedGenerationalDistance(pfTrue)
		metricList = [indicator(pf) for pf in pfList]
		rightList = numpy.loadtxt(os.path.join(pathOptimizer, 'IGD.csv')).tolist()
		self.assertGreater(scipy.stats.ttest_ind(rightList, metricList)[1], 0.05, [numpy.mean(rightList), numpy.mean(metricList), metricList])

if __name__ == '__main__':
	unittest.main()