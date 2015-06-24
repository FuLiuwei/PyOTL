/*!
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
*/

#pragma once

#include <pyotl/optimizer.integer/Global.h>

namespace pyotl
{
namespace optimizer
{
namespace couple
{
namespace integer
{
typedef pyotl::optimizer::integer::TProblem TProblem;
typedef pyotl::crossover::integer::TCoupleCrossover TCrossover;
typedef pyotl::optimizer::integer::TMutation TMutation;

typedef pyotl::optimizer::integer::TDecision TDecision;
typedef pyotl::optimizer::integer::TSolution TSolution;
typedef pyotl::optimizer::integer::TOptimizer TOptimizer;
}
}
}
}