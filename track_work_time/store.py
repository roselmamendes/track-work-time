from sqlalchemy import (
    Column,
    Integer,
    Date,
    func,
    String,
    ForeignKey,
    create_engine
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker

Base = declarative_base()


class WorkUnit(Base):
    __tablename__ = 'workunit'

    id = Column(Integer, primary_key=True)
    name = Column(String)


class WeekDay(Base):
    __tablename__ = 'weekday'

    id = Column(Integer, primary_key=True)
    day = Column(Date, default=func.now())
    hours = Column(Integer)
    workunit_id = Column(Integer, ForeignKey('workunit.id'))
    workunit = relationship(
        WorkUnit, backref=backref('weekdays', uselist=True)
    )


engine = create_engine('sqlite:///sqlalchemy_example.db')
Base.metadata.create_all(engine)

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()


def get_work_unit(work_unit_name):
    work_unit_found = session.query(WorkUnit).filter(
        WorkUnit.name == work_unit_name
    ).all()

    return work_unit_found[0] if work_unit_found else None


def set_work_unit(name):
    work_unit = WorkUnit(name=name)
    session.add(work_unit)
    session.commit()


def get_work_units():
    return session.query(WorkUnit).all()


def set_week_day(day, hours, work_unit):
    week_day = WeekDay(
        day=day,
        hours=hours,
        workunit_id=work_unit.id
    )
    session.add(week_day)
    session.commit()


def get_week_days_from(work_unit_name):
    work_unit = get_work_unit(work_unit_name)

    if work_unit is None:
        return None

    return work_unit.weekdays


def delete_all_on_db():
    session.query(WorkUnit).delete()
    session.query(WeekDay).delete()
