from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict

from animals import Animal, Mammal, Bird, Reptile, ValidationError
from enclosures import Enclosure
from staff import Zookeeper, Veterinarian


@dataclass
class Zoo:
    name: str
    animals: List[Animal] = field(default_factory=list)
    enclosures: List[Enclosure] = field(default_factory=list)
    staff: List[object] = field(default_factory=list)

    def add_animal(self, animal: Animal) -> None:
        self.animals.append(animal)

    def remove_animal(self, animal: Animal) -> None:
        self.animals.remove(animal)

    def add_enclosure(self, enclosure: Enclosure) -> None:
        self.enclosures.append(enclosure)

    def add_staff(self, member: object) -> None:
        self.staff.append(member)

    def assign_animal_to_enclosure(self, animal: Animal, enclosure: Enclosure) -> None:
        if animal.under_treatment:
            raise ValidationError("Animal under treatment cannot be moved.")
        if enclosure.can_accept(animal):
            enclosure.add_animal(animal)
        else:
            raise ValidationError("Enclosure cannot accept this animal.")

    # Simple daily routine scheduler that returns a list of strings describing tasks
    def daily_routine(self) -> List[str]:
        tasks: List[str] = []
        # Feeding
        zookeepers = [s for s in self.staff if isinstance(s, Zookeeper)]
        if zookeepers:
            zk = zookeepers[0]
            for e in zk.assigned_enclosures:
                for a in e.animals:
                    tasks.append(zk.feed(a))
        # Cleaning
        for zk in zookeepers:
            for e in zk.assigned_enclosures:
                tasks.append(zk.clean_enclosure(e))
        return tasks

    # Reports
    def animals_by_species(self) -> Dict[str, List[str]]:
        result: Dict[str, List[str]] = {}
        for a in self.animals:
            result.setdefault(a.species, []).append(a.name)
        return result

    def enclosure_status_report(self) -> List[str]:
        return [e.status() for e in self.enclosures]

    def health_report(self) -> List[str]:
        lines: List[str] = []
        for a in self.animals:
            active = [r for r in a.health_records if r.active]
            if active:
                lines.append(f"{a.name} ({a.species}) has {len(active)} active issue(s).")
        return lines
